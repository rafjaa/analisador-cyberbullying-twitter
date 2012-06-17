# coding: utf-8

import json
import pickle
import re
import thomas
import twitter


def persiste_tweets(num_dia, dia_semana):
    '''
        Realiza a busca, pré-processamento e armazenamento
        dos tweets que atendam aos critérios definidos.
    '''
    professor = list(set(twitter.buscar_tweets('meu professor', resultados=100, paginas=15, tipo='recent', data='{0} Apr 2012'.format(num_dia))))
    professora = list(set(twitter.buscar_tweets('minha professora', resultados=100, paginas=15, tipo='recent', data='{0} Apr 2012'.format(num_dia))))
    professor.sort(key=lambda t: t[-1])
    professora.sort(key=lambda t: t[-1])
    pickle.dump(professor, open('tweets/{0}.professor.pickle'.format(dia_semana), 'wb'))
    pickle.dump(professora, open('tweets/{0}.professora.pickle'.format(dia_semana), 'wb'))


def hora(h):
    '''
        Filtra o horário dos tweets.
    '''
    ho = int(re.search(r' (\d\d):', h).group(1))
    if ho >= 12 and ho < 18:
        return True
    return False


def processa():
    '''
        Realiza a classificação dos tweets armazenados utilizando
        o Filtro Bayesiano treinado e armazena o resultado em um
        formato de dados legível pela biblioteca gráfica D3.js.
    '''
    g = thomas.Bayes()
    g.load('treinamento/treino.dat')

    dias = {"Domingo": ('dom.professor.pickle', 'dom.professora.pickle'),
            "Segunda": ('seg.professor.pickle', 'seg.professora.pickle'),
            "Terça": ('ter.professor.pickle', 'ter.professora.pickle'),
            "Quarta": ('qua.professor.pickle', 'qua.professora.pickle'),
            "Quinta": ('qui.professor.pickle', 'qui.professora.pickle'),
            "Sexta": ('sex.professor.pickle', 'sex.professora.pickle'),
            "Sábado": ('sab.professor.pickle', 'sab.professora.pickle'),
    }
    tweets = {"name": "", "children": []}
    total_tw_dias = 0

    for dia in dias:
        m = dias[dia][0]
        f = dias[dia][1]

        dados_m = [d for d in pickle.load(open('tweets/' + m)) if hora(d[-1])]
        dados_f = [d for d in pickle.load(open('tweets/' + f)) if hora(d[-1])]
        tweets_dia = len(dados_m + dados_f)
        total_tw_dias += tweets_dia

        classif_m = {'POS': 0, 'NEG': 0, 'NEU': 0}
        classif_f = {'POS': 0, 'NEG': 0, 'NEU': 0}

        for t in dados_m:
            classif = thomas.classifica(g.guess(t[1]))
            total = t[2]
            classif_m[classif] += total

        for t in dados_f:
            classif = thomas.classifica(g.guess(t[1]))
            total = t[2]
            classif_f[classif] += total       

        l = {"name": "{0} ({1})".format(dia, tweets_dia), "children": [
               {"name": 'Professor ({0})'.format(len(dados_m)), "children": [{"name": "Positivo: {0} tweets".format(classif_m['POS'])}, {"name": "Negativo: {0} tweets".format(classif_m['NEG'])}, {"name": "Neutro: {0} tweets".format(classif_m['NEU'])}]},
               {"name": 'Professora ({0})'.format(len(dados_f)), "children": [{"name": "Positivo: {0} tweets".format(classif_f['POS'])}, {"name": "Negativo: {0} tweets".format(classif_f['NEG'])}, {"name": "Neutro: {0} tweets".format(classif_f['NEU'])}]}
            ]}

        tweets['children'].append(l)

    tweets['name'] = "{0} Tweets".format(total_tw_dias)
    json.dump(tweets, open('grafico/arvore.json','wb'))


if __name__ == '__main__':
    #persiste_tweets(01, 'dom')
    #persiste_tweets(02, 'seg')
    #persiste_tweets(03, 'ter')
    #persiste_tweets(04, 'qua')
    #persiste_tweets(05, 'qui')
    #persiste_tweets(06, 'sex')
    #persiste_tweets(07, 'sab')
    processa()