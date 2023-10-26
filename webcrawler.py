import requests
from bs4 import BeautifulSoup
from datetime import date
import time
import schedule
from database import Database
from bot import BOT


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
        for h in range(len(tempmin)):
            tempmin[h] = tempmin[h].text  # separa somente o texto da temperatura
            tempmin[h] = tempmin[h].strip('°')
            tempmin[h] = int(tempmin[h].strip('°º '))

        # procura pelas temperaturas máximas
        tempmax = (inicial.findAll('span', {'class': 'max changeUnitT'}))

        for h in range(len(tempmax)):
            tempmax[h] = tempmax[h].text  # separa somente o texto da temperatura
            tempmax[h] = int(tempmax[h].strip('°º '))

        # procura pelas chances de chuva
        chancechuva = (inicial.findAll('span', {'class': 'txt-strng probabilidad center'}))
        for h in range(len(chancechuva)):
            chancechuva[h] = chancechuva[h].text  # separa somente o texto da chance
            chancechuva[h] = int(chancechuva[h].strip('°º% '))
        previsao_dia = {}
        for h in range(3):  # organiza as informações de 3 dias em um dicionário e adiciona ele a lista de previsões
            try:
                previsao_dia['tmax'] = tempmax[h]
                previsao_dia['tmin'] = tempmin[h]
            except IndexError:
                print('Tempo não tem temperatura para', h)

            try:
                previsao_dia['chuva'] = chancechuva[h]
            except IndexError:
                print('Tempo não tem chance de chuva para', h)

            try:
                previsoes.append(previsao_dia)
            except IndexError:
                print('nada em tempo')

        print('Tempo:')  # da print em cada dícionario da lista de previsões
        for h in previsoes:
            print(h)

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

        '''induv = inicial.find('span', {'data-testid': 'UVIndexValue'})
        print(induv)
        for i in range(len(induv)):
            induv = induv.text
            induv = induv[0:2]
            induv = int(induv.strip('of '))
            print(induv, ' indicie UV')'''

        for i in range(3):
            previsao_dia = {
                'tmax': tempmax[i],
                'tmin': tempmin[i],
                'chuva': chancechuva[i]
            }
            previsoes.append(previsao_dia)
        # previsoes[0]['ind_uv'] = induv

        print('Weather:')
        for i in previsoes:
            print(i)

        return previsoes

    def procura_em_tutiempo(self):
        inicial = self.info('https://pt.tutiempo.net/indice-ultravioleta/feira-de-santana.html')

        previsoes = []

        ind_uv_h = inicial.findAll('span', {'class': 'ener'})

        ind_uv = [ind_uv_h[0:10], ind_uv_h[10:20], ind_uv_h[20:30]]

        horas = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16]  # horas que aparecem no site para cada valor UV

        for i in range(len(ind_uv)):
            for h in range(len(ind_uv[i])):
                ind_uv[i][h] = int(ind_uv[i][h].text)

            previsao_dia = {
                'ind_uv': max(ind_uv[i]),
                'h_uv': horas[ind_uv[i].index(max(ind_uv[i]))]  # usa o indice do uv maximo para saber a hora
                # hora do maximo indicie UV do dia
            }

            previsoes.append(previsao_dia)

        return previsoes

    # organiza as informações dos sites em uma só lista fazendo a média das temperaturas e chances de chuva
    def organiza_informacoes(self):  # g1 dava valores muito diferentes para temperatura, por isso foi tirado
        info = [self.procura_em_tempo(), self.procura_em_cptec(), self.procura_em_wather(),
                self.procura_em_tutiempo()]
        info_organizada = []
        dias = [(date.today().strftime('%d-%m-%Y')), 'amanha', 'depois']

        for dia in range(3):
            n_sites_chuva = 0
            n_sites_temp = 0
            n_sites_uv = 0
            previsao_dia = {
                'tmax': 0,
                'tmin': 0,
                'chuva': 0,
                'dia': dias[dia]
            }
            for site in info:
                if 'tmax' in site[dia] and 'tmin' in site[dia]:
                    previsao_dia['tmax'] += site[dia]['tmax']
                    previsao_dia['tmin'] += site[dia]['tmin']
                    n_sites_temp += 1
                if 'chuva' in site[dia]:
                    previsao_dia['chuva'] += site[dia]['chuva']
                    n_sites_chuva += 1
                if 'ind_uv' in site[dia]:
                    previsao_dia['ind_uv'] = site[dia]['ind_uv']
                    previsao_dia['h_uv'] = site[dia]['h_uv']
                    n_sites_uv += 1

            previsao_dia['tmax'] //= n_sites_temp
            previsao_dia['tmin'] //= n_sites_temp
            previsao_dia['chuva'] //= n_sites_chuva
            previsao_dia['ind_uv'] //= n_sites_uv

            # a formatação dos valores agora será no bot.py
            '''
            previsao_dia['tmax'] = str(previsao_dia['tmax']) + '°'

            previsao_dia['tmin'] = str(previsao_dia['tmin']) + '°'

            previsao_dia['chuva'] = str(previsao_dia['chuva']) + '%' '''

            info_organizada.append(previsao_dia)

        print('\nprevisão média:')
        for i in info_organizada:
            print(i)

        # por enquanto não da return nas informações, deve ser colocado depois para que outra função coloque no banco
        return info_organizada

    def tarefas_diarias(self, db, bot):
        previsoes = crawler.organiza_informacoes()

        for dia in previsoes:
            db.nova_previsao(dia)

        bot.post(previsoes[0])


if __name__ == '__main__':
    crawler = Crawler()
    db = Database()
    bot = BOT()

    previsoes = crawler.organiza_informacoes()
    for dia in previsoes:
        db.nova_previsao(dia)
        print('foi', dia)

    bot.post(previsoes[0])

    # por enquanto o agendamento do horário está como comentário para facilitar testes, mas está funcionando!
    '''
    schedule.every().day.at("05:00").do(crawler.tarefas_diarias, db, bot)  # pega a previsão do tempo as 05h

    while True:
        schedule.run_pending()
        time.sleep(1)'''
