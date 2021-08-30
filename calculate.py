import pandas as pd
from dotenv import dotenv_values

config = dotenv_values(".env")
usersSpy = config["SPY_ACCOUNTS"].split(',')
dados = pd.read_json("data/dados.json", orient='table')

for user in usersSpy:
    userData = dados.loc[dados['username'] == user, ['qntSeguidores', 'qntSeguindo', 'posts', 'date']]
    for index, user in userData.iterrows():
        user['date'] = pd.to_datetime(user['date'], utc=True)
        ordenado = userData.sort_values(by=["date"], ascending=False)
        filter = ordenado.loc['qntSeguidores', 'qntSeguindo', 'posts']
    #diference = filter.diff(axis=1)
    #print(diference)