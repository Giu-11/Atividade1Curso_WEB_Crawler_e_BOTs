from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os


class Database:

    def __init__(self):  # inicia o banco de dados e o env
        load_dotenv()
        self.previsoes = self.connect()

    def connect(self):
        cliente = MongoClient(os.getenv('DB_URL'))
        db = cliente['tempo']
        return db.tempo

    def nova_previsao(self, previsao: dict):
        procura = {'dia': previsao['dia']}
        result = self.previsoes.find_one(procura)

        if result is None:
            return self.previsoes.insert_one(previsao)

        elif previsao['dia'] == 'amanha' or previsao['dia'] == 'depois':
            if previsao['tmax'] != result['tmax'] and previsao['tmin'] != result['tmin'] and previsao['chuva'] != result['chuva']:
                self.previsoes.replaceOne({'dia': previsao['dia']}, previsao)

    def procura(self, dia):
        procura = {'dia': dia}
        result = self.previsoes.find_one(procura)

        if result is None:
            print('informação não encontrada para dia', dia)
        else:
            print('A temperatura máxima para', result['dia'], ' é de', result['tmax'], ' a minima de', result['tmin'],
                  ' e há uma chance de', result['chuva'], ' de chover')
