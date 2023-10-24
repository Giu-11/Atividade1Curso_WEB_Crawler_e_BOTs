import tweepy
from dotenv import load_dotenv
import os


class BOT:
    def __init__(self):
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
        texttemperatura = '  • não foi possivel obter dados da temperatura \U0001F630\n'
        textchuva = '  • não foi possivel obter dados da chance de chuva \U0001F610'

        if 'chuva' in info:
            textchuva = ' • A chance de chuva para hoje é de ' + str(info['chuva']) + '%'
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

        if 'tmax' in info and 'tmin' in info:
            texttemperatura = '\U0001F321 • temperatura máxima é de ' + str(info['tmax']) + '° \U0001F525'
            texttemperatura += 'e a mínima de ' + str(info['tmin']) + '° \U00002744 \n'

        full_text = texttemperatura+textchuva
        c = self.client
        c.create_tweet(text=full_text)
