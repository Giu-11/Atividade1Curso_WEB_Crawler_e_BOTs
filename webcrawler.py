import requests
from bs4 import BeautifulSoup
from datetime import date
import schedule
from database import Database


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

        # procura pelas temperaturas mínimas
        tempmin = inicial.findAll('span', {'class': 'min changeUnitT'})
        for i in range(len(tempmin)):
            tempmin[i] = tempmin[i].text  # separa somente o texto da temperatura
            tempmin[i] = tempmin[i].strip('°')
            tempmin[i] = int(tempmin[i].strip('°º '))

        # procura pelas temperaturas máximas
        tempmax = (inicial.findAll('span', {'class': 'max changeUnitT'}))
        for i in range(len(tempmax)):
            tempmax[i] = tempmax[i].text  # separa somente o texto da temperatura
            tempmax[i] = int(tempmax[i].strip('°º '))

        # procura pelas chances de chuva
        chancechuva = (inicial.findAll('span', {'class': 'txt-strng probabilidad center'}))
        for i in range(len(chancechuva)):
            chancechuva[i] = chancechuva[i].text  # separa somente o texto da chance
            chancechuva[i] = int(chancechuva[i].strip('°º% '))

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

        return previsoes

    def procura_em_cptec(self):
        inicial = self.info('https://www.cptec.inpe.br/previsao-tempo/ba/feira-de-santana')

        previsoes = []

        tempmin = inicial.findAll('span', {'class': 'text-primary text-left font-weight-bold pull-left h5'})

        for i in range(len(tempmin)):
            tempmin[i] = tempmin[i].text
            tempmin[i] = tempmin[i][1:4]  # retira alguns caracteres extras para ter somente a temperatura
            tempmin[i] = int(tempmin[i].strip('°º '))

        tempmax = (inicial.findAll('span', {'class': 'text-danger text-right font-weight-bold pull-right h5'}))

        for i in range(len(tempmax)):
            tempmax[i] = tempmax[i].text
            tempmax[i] = tempmax[i][0:3]
            tempmax[i] = int(tempmax[i].strip('°º '))

        for i in range(3):
            previsao_dia = {
                'tmax': tempmax[i],
                'tmin': tempmin[i],
            }
            previsoes.append(previsao_dia)

        print('CPTEC:')
        for i in previsoes:
            print(i)

        return previsoes

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
            tempmax[i] = int(tempmax[i].strip('°º '))

        for i in range(len(tempmin)):
            tempmin[i] = tempmin[i].text
            tempmin[i] = tempmin[i][1:4]
            tempmin[i] = int(tempmin[i].strip('°º '))

        for i in range(3):
            previsao_dia = {
                'tmax': tempmax[i],
                'tmin': tempmin[i]
            }
            previsoes.append(previsao_dia)

        print('G1:')
        for i in previsoes:
            print(i)

        return previsoes

    def procura_em_wather(self):
        inicial = self.info('https://weather.com/weather/today/l/-12.25,-38.96')

        previsoes = []

        tempmin = inicial.findAll('div', {'data-testid': 'SegmentLowTemp'})
        tempmin = tempmin[0:3]

        for i in range(len(tempmin)):
            tempmin[i] = tempmin[i].text
            tempmin[i] = int(tempmin[i].strip('°º '))
            tempmin[i] = round((tempmin[i] - 32) * 5 / 9)
            # esse site devolve as temperaturas em Fahrenheit
            # podem ter leves variações na temperatura que o código mostra e o que aparece no site

        tempmax = inicial.findAll('div', {'data-testid': 'SegmentHighTemp'})
        tempmax = tempmax[10:13]

        for i in range(len(tempmax)):
            tempmax[i] = tempmax[i].text
            tempmax[i] = int(tempmax[i].strip('°º '))
            tempmax[i] = round((tempmax[i] - 32) * 5 / 9)

        chancechuva = inicial.findAll('span', {'class': 'Column--precip--3JCDO'})
        chancechuva = chancechuva[9:12]
        for i in range(len(chancechuva)):
            chancechuva[i] = chancechuva[i].text
            chancechuva[i] = int(chancechuva[i].strip('Chance of Rain°º %'))

        for i in range(3):
            previsao_dia = {
                'tmax': tempmax[i],
                'tmin': tempmin[i],
                'chuva': chancechuva[i]
            }
            previsoes.append(previsao_dia)

        print('Weather:')
        for i in previsoes:
            print(i)

        return previsoes

    # organiza as informações dos sites em uma só lista fazendo a média das temperaturas e chances de chuva
    def organiza_informacoes(self):
        info = [self.procura_em_tempo(), self.procura_em_cptec(), self.procura_em_g1(), self.procura_em_wather()]
        n_sites = len(info)
        info_organizada = []
        dias = [(date.today().strftime('%d-%m-%Y')), 'amanha', 'depois']

        for dia in range(3):
            n_sites_chuva = 0
            previsao_dia = {
                'tmax': 0,
                'tmin': 0,
                'chuva': 0,
                'dia': dias[dia]
            }
            for site in info:
                previsao_dia['tmax'] += site[dia]['tmax']
                previsao_dia['tmin'] += site[dia]['tmin']
                if 'chuva' in site[dia]:
                    previsao_dia['chuva'] += site[dia]['chuva']
                    n_sites_chuva += 1

            previsao_dia['tmax'] //= n_sites
            previsao_dia['tmax'] = str(previsao_dia['tmax'])+'°'

            previsao_dia['tmin'] //= n_sites
            previsao_dia['tmin'] = str(previsao_dia['tmin'])+'°'

            previsao_dia['chuva'] //= n_sites_chuva
            previsao_dia['chuva'] = str(previsao_dia['chuva'])+'%'

            info_organizada.append(previsao_dia)
        
        print('\nprevisão média:')
        for i in info_organizada:
            print(i)

        # por enquanto não da return nas informações, deve ser colocado depois para que outra função coloque no banco
        return info_organizada


if __name__ == '__main__':

    crawler = Crawler()
    db = Database()

    previsoes = crawler.organiza_informacoes()
    for dia in previsoes:
        db.nova_previsao(dia)

    # por enquanto o agendamento do horário está como comentário para facilitar testes, mas está funcionando!
    '''schedule.every().day.at("05:00").do(crawler.organiza_informacoes)  # pega a previsão do tempo as 05h
    while True:
        schedule.run_pending()'''
