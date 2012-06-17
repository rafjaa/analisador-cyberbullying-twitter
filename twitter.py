# coding: utf-8

import json
import re
import urllib2
from unicodedata import normalize


def preprocessa_tweet(tweet):
    '''
        Realiza um preprocessamento do tweet fornecido, para otimizar
        o desempenho do filtro de classificação e remover informações
        pessoais dos usuários.
    '''
    MIN_LETRAS = 3
    MAX_LETRAS = 16
    INDIFERENTE = set(('que', 'qual', 'ele', 'ela', 'dos', 'das', 'vou', 'ver', 'com', 'era', 'para', 'pro', 'pra', 'mas', 'ou'))

    sem_acento = normalize('NFKD', tweet).encode('ASCII','ignore')
    caracteres_extra = re.compile(r'[^ ]*@[^ ]*|#|http[^ ]+|\d+|\.|\*|\?|\+|\(|\)|\"|\'|~|^|´|`|,|:|;|!|-|_|/|=|&')

    return ' '.join([p for p in caracteres_extra.sub('', sem_acento).split() if MIN_LETRAS <= len(p) <= MAX_LETRAS and p not in INDIFERENTE])


def buscar_tweets(termo, resultados=10, paginas=10, tipo='recent', data=''):
    '''
        Busca n tweets contendo o termo de busca fornecido.

        A data deve ser uma string do tipo: 31 Mar 2012

        Retorna uma lista de tuplas contendo o texto original do
        tweet,o texto preprocessado, o número de ocorrências do
        mesmo (1 + número de retweets) e o horário.

        Por questões de privacidade não armazena o código identificador
        do tweet nem informações sobre usuários, inclusive menções do
        tipo @usuario.

        API: https://dev.twitter.com/docs/api/1/get/search
    '''
    url_api = 'http://search.twitter.com/search.json?q="{0}"&rpp={1}&page={2}&result_type={3}'
    tweets = []

    for num_pagina in xrange(1, paginas + 1):
        resposta = urllib2.urlopen(url_api.format('%20'.join(termo.split()), resultados, num_pagina, tipo)).read()
        for tw in json.loads(resposta)['results']:
            if data.lower() in tw['created_at'].lower():
                retweets = tw['metadata']['recent_retweets'] if 'recent_retweets' in tw['metadata'] else 0
                # Remove o próprio termo de busca, pois será desnecessário na análise
                texto = tw['text'].lower().replace(termo, '')
                tweets.append((tw['text'], preprocessa_tweet(texto), 1 + retweets, tw['created_at'].lower()))

    return tweets