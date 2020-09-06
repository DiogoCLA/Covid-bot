import time
import tweepy
import urllib.request
import json
import os

numCasos = 0

# urlPais = "https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalGeralApi"
# responsePais = urllib.request.urlopen(urlPais)
# dataPais = json.loads(responsePais.read())

print("Getting data")
""" Get Information from the states """
urlEstado = "https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalEstado"
responseEstado = urllib.request.urlopen(urlEstado)
dataEstado = json.loads(responseEstado.read())

"""Find specific information for RN"""
for i in dataEstado:
    if i['_id'] == 'RN':
        casosRN = i['casosAcumulado']
        obitosRN = i['obitosAcumulado']
        break

"""Get information from the cities"""
urlCidade = "https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalMunicipio"
responseCidade = urllib.request.urlopen(urlCidade)
dataCidade = json.loads(responseCidade.read())

"""Get specific information from Natal and Mossoró"""
for i in dataCidade:
    if i['_id'] == 'Natal':
        casosNatal = i['casosAcumulado']
        obitosNatal = i['obitosAcumulado']

    if i['_id'] == 'Mossoró':
        casosMossoro = i['casosAcumulado']
        obitosMossoro = i['obitosAcumulado']

        break

"""forever"""
while True:
    if numCasos != casosRN:
        # Authenticate to Twitter
        auth = tweepy.OAuthHandler("FPOBGYWC4royZB80Dichq0yRP",
                                   os.environ['APISECRETKEY'])
        auth.set_access_token("1290022466002321413-ylhFNcnnukDJMqEYkA2i45g6EmQ40s",
                              os.environ['ACCESSTOKENSECRET'])

        # Create API object
        api = tweepy.API(auth, wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True)

        string = "Casos Confirmados no RN: " + str(casosRN) + "\nCasos Confirmados em Natal: "
        string = string + str(casosNatal) + "\nCasos Confirmados em Mossoró: " + str(casosMossoro)

        # post it to twitter
        print ("updating cases")
        api.update_status(string)

        numCasos = casosRN

    else:
        print("no change")
    time.sleep(3600)
