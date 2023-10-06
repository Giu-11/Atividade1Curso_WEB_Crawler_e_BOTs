import requests
from bs4 import BeautifulSoup


class Crawler:
    @staticmethod
    def info(link: str):
        resposta = requests.get(link)
        sopa = BeautifulSoup(resposta.text, 'html.parser')  # pega o código html da página
        return sopa

    # somente a primeira função de pegar informações está comentada já que o funcionamento das 3 é idêntico
    def procura_em_tempo(self):
        inicial = self.info('https://www.tempo.com/feira-de-santana.htm')

        previsoes = []  # lista que vai guardar todas as informações da previsão de hoje e os próximos 2 dias

        #procura pelas temperaturas mínimas
        tempmin = inicial.findAll('span', {'class': 'min changeUnitT'})
        for i in range(len(tempmin)):
            tempmin[i] = tempmin[i].text  # separa somente o texto da temperatura

        # procura pelas temperaturas máximas
        tempmax = (inicial.findAll('span', {'class': 'max changeUnitT'}))
        for i in range(len(tempmax)):
            tempmax[i] = tempmax[i].text  # separa somente o texto da temperatura

        # procura pelas chances de chuva
        chancechuva = (inicial.findAll('span', {'class': 'txt-strng probabilidad center'}))
        for i in range(len(chancechuva)):
            chancechuva[i] = chancechuva[i].text # separa somente o texto da chance

        for i in range(3):  # organiza as informações de 3 dias em um dicionário e adiciona ele a lista de previsões
            previsao_dia = {
                'tmax': tempmax[i],
                'tmin': tempmin[i],
                'chuva': chancechuva[i]
            }
            previsoes.append(previsao_dia)

        print('Tempo:')  # da print em cada dícionario da lista de previsões
        for i in previsoes:
            print(i)

    def procura_em_cptec(self):
        inicial = self.info('https://www.cptec.inpe.br/previsao-tempo/ba/feira-de-santana')

        previsoes = []

        tempmin = inicial.findAll('span', {'class': 'text-primary text-left font-weight-bold pull-left h5'})

        for i in range(len(tempmin)):
            tempmin[i] = tempmin[i].text
            tempmin[i] = tempmin[i][1:4]

        tempmax = (inicial.findAll('span', {'class': 'text-danger text-right font-weight-bold pull-right h5'}))

        for i in range(len(tempmax)):
            tempmax[i] = tempmax[i].text
            tempmax[i] = tempmax[i][0:3]

        chancechuva = (inicial.findAll('div', {'class': 'col-md-12 mb-2 text-center align-middle text-primary'}))
        for i in range(len(chancechuva)):
            chancechuva[i] = chancechuva[i].text
            chancechuva[i] = chancechuva[i][19:23]

        for i in range(3):
            previsao_dia = {
                'tmax': tempmax[i],
                'tmin': tempmin[i],
                'chuva': chancechuva[i]
            }
            previsoes.append(previsao_dia)

        print('CPTEC:')
        for i in previsoes:
            print(i)

    def procura_em_g1(self):
        inicial = self.info('https://g1.globo.com/previsao-do-tempo/ba/feira-de-santana.ghtml')

        previsoes = []

        tempmax = inicial.findAll('div', {'class': 'forecast-today__temperature forecast-today__temperature--max'})
        tempmin = inicial.findAll('div', {'class': 'forecast-today__temperature forecast-today__temperature--min'})

        temp_proximos = (inicial.findAll('span', {'class': 'forecast-next-days__item-value'}))

        for i in range(len(temp_proximos)):
            if i % 2 == 0:
                tempmax.append(temp_proximos[i])
            else:
                tempmin.append(temp_proximos[i])

        for i in range(len(tempmax)):
            tempmax[i] = tempmax[i].text
            tempmax[i] = tempmax[i][1:4]

        for i in range(len(tempmin)):
            tempmin[i] = tempmin[i].text
            tempmin[i] = tempmin[i][1:4]

        for i in range(3):
            previsao_dia = {
                'tmax': tempmax[i],
                'tmin': tempmin[i]
            }
            previsoes.append(previsao_dia)

        print('G1:')
        for i in previsoes:
            print(i)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.procura_em_tempo()
    crawler.procura_em_cptec()
    crawler.procura_em_g1()
