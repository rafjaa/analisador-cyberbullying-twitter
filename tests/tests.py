# coding: utf-8

import json
import os.path
import sys
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import thomas
import twitter


class TesteClassificacaoTweets(unittest.TestCase):
    def setUp(self):
        # Instancia e carrega o classificador treinado
        self.classificador = thomas.Bayes()
        self.classificador.load('../treinamento/treino.dat')

        # Carrega os tweets para o teste e validação
        self.tweets_treino = json.load(open('../treinamento/tweets.treino.json'))
        self.tweets_validacao = json.load(open('../treinamento/tweets.validacao.json'))


    def teste_treinamento_classificador(self):
        total_tweets = len(self.tweets_treino)
        acertos = 0
        for tw in self.tweets_treino:
            texto = twitter.preprocessa_tweet(tw[0].lower())
            if thomas.classifica(self.classificador.guess(texto)) == tw[1]:
                acertos += 1
            else:
                self.classificador.train(tw[1], texto)
                self.classificador.save('../treinamento/treino.dat')

        self.assertTrue(acertos == total_tweets)


    def teste_validacao_classificador(self):
        total_tweets = len(self.tweets_validacao)
        acertos = 0
        for tw in self.tweets_validacao:
            texto = twitter.preprocessa_tweet(tw[0].lower())
            if thomas.classifica(self.classificador.guess(texto)) == tw[1]:
                acertos += 1

        # Exige um índice de acerto de pelo menos 80%
        self.assertTrue(acertos * 100 / total_tweets >= 80)


if __name__ == '__main__':
    unittest.main()