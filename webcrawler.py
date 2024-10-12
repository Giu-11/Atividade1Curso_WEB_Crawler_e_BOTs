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

    def procura_em_weather(self):
        inicial = self.info('https://weather.com/weather/today/l/ee246b22655e20e276a44c5bf48c45cf8a5ca72e7517e6463d8958135cfc8077')

        previsoes = []

        tempmin = inicial.findAll('div', {'data-testid': 'SegmentLowTemp'})
        tempmin = tempmin[0:3]

        for i in range(len(tempmin)):
            tempmin[i] = tempmin[i].text
            print(tempmin[i])
            tempmin[i] = int(tempmin[i].strip('°º '))
            tempmin[i] = round((tempmin[i] - 32) * 5 / 9)
            # esse site devolve as temperaturas em Fahrenheit
            # podem ter leves variações na temperatura que o código mostra e o que aparece no site

        tempmax = inicial.findAll('div', {'data-testid': 'SegmentHighTemp'})
        tempmax = tempmax[10:12]

        for i in range(len(tempmax)):
            #FIXME parece ter um erro com a 1 posição da temp maxima
            tempmax[i] = tempmax[i].text[:2]
            print(tempmax[i])
            tempmax[i] = int(tempmax[i].strip('°º '))
            tempmax[i] = round((tempmax[i] - 32) * 5 / 9)
        if len(tempmax)!=3:
            tempmax.insert(0, tempmax[1])

        chancechuva = inicial.findAll('span', {'class': 'Column--precip--YkErk'})
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
        inicial_t = self.info('https://pt.tutiempo.net/feira-de-santana.html')

        previsoes = []

        ind_uv_h = inicial.findAll('span', {'class': 'huv'})

        ind_uv_v = inicial.findAll('span', {'class': 'vuv'})

        #print(ind_uv_v, "\n", ind_uv_h)

        for i in range(len(ind_uv_v)):
            ind_uv_v[i] = ind_uv_v[i].text
            ind_uv_v[i] = int(ind_uv_v[i].strip('<span class="vuv"></span>'))

            ind_uv_h[i] = ind_uv_h[i].text
            ind_uv_h[i] = int(ind_uv_h[i].strip('<span class="huv"></span>::')[:2])

        ind_uv_h = [ind_uv_h[:9], ind_uv_h[9:19], ind_uv_h[19:29]]
        ind_uv_v = [ind_uv_v[:9], ind_uv_v[9:19], ind_uv_v[19:29]]

        #print(ind_uv_v, "\n", ind_uv_h)
        temp = [inicial_t.findAll('div', {'class': 'dn1 sel'})[0],
                inicial_t.findAll('div', {'class': 'dn2'})[0],
                inicial_t.findAll('div', {'class': 'dn3'})[0]]
        #print(temp)

        tmax = []
        tmin = []
        for i in range(len(temp)):
            temp[i] = temp[i].text[10:].lower().strip("abcdefghijklmnopqrstuvwxyz°°°º  ")
            tmax.append(int(temp[i][:2]))
            tmin.append(int(temp[i][3:]))
            #print(temp[i])

        for i in range(3):
            print(ind_uv_h[i])
            print(ind_uv_v[i])

            previsao_dia = {
                'tmax': tmax[i],
                'tmin': tmin[i],
                'ind_uv': max(ind_uv_v[i]),
                'h_uv': ind_uv_h[i][ind_uv_v[i].index(max(ind_uv_v[i]))]  # usa o indice do uv maximo para saber a hora
                # hora do maximo indicie UV do dia
            }
            previsoes.append(previsao_dia)

        print('tutiempo:')
        for i in previsoes:
            print(i)

        return previsoes

    # organiza as informações dos sites em uma só lista fazendo a média das temperaturas e chances de chuva
    def organiza_informacoes(self):
        # g1 dava valores muito diferentes para temperatura, por isso foi tirado
        # o mesmo para o weather e tempo
        info = [self.procura_em_cptec(), self.procura_em_weather(), self.procura_em_tutiempo()]
        try:
            info.append(self.procura_em_cptec())
        except:
            print("deu ruim cptec")

        try:
            info.append(self.procura_em_weather())
        except:
            print("deu ruim weather")

        try:
            info.append(self.procura_em_tutiempo())
        except:
            print("deu ruim tutiempo")

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

            if n_sites_temp > 0:
                previsao_dia['tmax'] //= n_sites_temp
                previsao_dia['tmin'] //= n_sites_temp

            if n_sites_chuva > 0:
                previsao_dia['chuva'] //= n_sites_chuva

            if n_sites_uv > 0:
                previsao_dia['ind_uv'] //= n_sites_uv

            info_organizada.append(previsao_dia)

        print('\nprevisão média:')
        for i in info_organizada:
            print(i)

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

    #aa = crawler.procura_em_cptec()

    aa= crawler.procura_em_weather()

    """previsoes = crawler.organiza_informacoes()
    for dia in previsoes:
        db.nova_previsao(dia)
        print('foi', dia)"""

    #bot.post(previsoes[0])

    # por enquanto o agendamento do horário está como comentário para facilitar testes, mas está funcionando!
    '''
    schedule.every().day.at("05:03").do(crawler.tarefas_diarias, db, bot)  # pega a previsão do tempo as 05h

    while True:
        schedule.run_pending()
        time.sleep(1)'''
