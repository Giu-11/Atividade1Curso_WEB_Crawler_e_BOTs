import tweepy
from dotenv import load_dotenv
import os


class BOT:
    def __init__(self):  # faz a conexão com a api do twitter usando as senhas e chaves
        load_dotenv()
        consumer_key = os.getenv('TWT_CONSUMER_KEY')
        consumer_secret = str(os.getenv('TWT_CONSUMER_SECRET'))
        access_token = str(os.getenv('TWT_ACCESS_TOKEN'))
        access_token_secret = str(os.getenv('TWT_ACCESS_TOKEN_SECRET'))

        self.client = tweepy.Client(
            #bearer_token=r"{}".format(os.getenv('TWT_BARER_TOKEN')),
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        '''auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
        auth.set_access_token(
            access_token,
            access_secret
        )
        self.api = tweepy.API(auth)'''

    def post(self, info: dict):
        #textos iniciais para caso haja um erro com as informações
        texttemperatura = '  • não foi possivel obter dados da temperatura \U0001F630\n'
        textchuva = '  • não foi possivel obter dados da chance de chuva \U0001F610'
        textuv = '  • não foi possivel obter dados da chance do indicie UV \U0001F627'

        if 'chuva' in info:  # muda o texto e emojis para a chance de chuva de acordo com valor
            textchuva = ' • A chance de chuva para hoje é de ' + str(info['chuva']) + '%\n'
            if info['chuva'] <= 20:
                textchuva = '\U00002600' + textchuva
            elif info['chuva'] <= 40:
                textchuva = '\U0001F324' + textchuva
            elif info['chuva'] <= 60:
                textchuva = '\U0001F325' + textchuva
            elif info['chuva'] <= 80:
                textchuva = '\U00002601' + textchuva
            elif info['chuva'] <= 100:
                textchuva = '\U0001F327' + textchuva

        if 'tmax' in info and 'tmin' in info: # monta o texto para a temperatura
            texttemperatura = '\U0001F321 • temperatura máxima é de ' + str(info['tmax']) + '° \U0001F525'
            texttemperatura += 'e a mínima de ' + str(info['tmin']) + '° \U00002744\n'

        if 'ind_uv' in info:  # ajusta o texto sobre o indicie uv de acordo com o valor dele
            textuv = '\U0001F506 • O índicie UV máximo é de ' + str(info['ind_uv']) + ' as ' + str(info['h_uv']) + 'h\n'
            if 1 <= info['ind_uv'] <= 2:
                textuv += '\U0001F44D é seguro sair no sol hoje'
            elif 3 <= info['ind_uv'] <= 5:
                textuv += '\U000026A0 é indicado o uso de camisa, óculos de sol e protetor solar'
            elif 6 <= info['ind_uv'] <= 7:
                textuv += '\U000026A0 é indicado o uso de chapéu, camisa, óculos de sol e protetor solar, evite tomar ao meio dia'
            elif 8 <= info['ind_uv'] <= 10:
                textuv += '\U000026A0 é indicado o uso de chapéu, camisa, óculos de sol e protetor solar mesmo na sombra das 11 as 16h'
            elif 11 <= info['ind_uv']:
                textuv += '\U000026A0 é indicado o uso de chapéu, camisa, óculos de sol e protetor solar mesmo na sombra, evite sair de casa das 11 as 16h'

        full_text = texttemperatura+textchuva+textuv  # junta os textos
        c = self.client
        #c.create_tweet(text=full_text)  # postas as informações
        print('\n', full_text)
