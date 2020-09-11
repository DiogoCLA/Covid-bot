import time
import tweepy
import urllib.request
import json
import os


def main():
    numCasosRN = 0
    numCasosNatal = 0
    numCasosMossoro = 0

    # urlPais = "https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalGeralApi"
    # responsePais = urllib.request.urlopen(urlPais)
    # dataPais = json.loads(responsePais.read())

    """forever"""
    while True:
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

        diffRN = casosRN - numCasosRN
        diffNatal = casosNatal - numCasosNatal
        diffMossoro = casosMossoro - numCasosMossoro
        if 0 < diffRN < 10000:
            if 0 < diffNatal < 10000:
                if 0 < diffMossoro < 5000:
                    # Authenticate to Twitter
                    auth = tweepy.OAuthHandler("FPOBGYWC4royZB80Dichq0yRP",
                                               os.environ['APISECRETKEY'])
                    auth.set_access_token("1290022466002321413-ylhFNcnnukDJMqEYkA2i45g6EmQ40s",
                                          os.environ['ACCESSTOKENSECRET'])

                    # Create API object
                    api = tweepy.API(auth, wait_on_rate_limit=True,
                                     wait_on_rate_limit_notify=True)

                    string = "Casos Confirmados no RN: " + str(casosRN) + "(+" + str(
                        diffRN) + ")" + "\nCasos Confirmados em Natal: "
                    string = string + str(casosNatal) + "(+" + str(
                        diffNatal) + ")" + "\nCasos Confirmados em Mossoró: " + str(casosMossoro) + "(+" + str(
                        diffMossoro) + ")"

                    # post it to twitter
                    print("updating cases")
                    api.update_status(string)

        else:
            print("no change")

        numCasosRN = casosRN
        numCasosNatal = casosNatal
        numCasosMossoro = casosMossoro

        time.sleep(28800)


main()
