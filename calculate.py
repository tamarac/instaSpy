import pandas as pd
from dotenv import dotenv_values
from datetime import datetime, timedelta
from sendEmail import send
config = dotenv_values(".env")
usersSpy = config["SPY_ACCOUNTS"].split(',')
dados = pd.read_json("data/dados2.json", orient='table')

for user in usersSpy:
    dados['date'] = pd.to_datetime(dados.date, format='%Y-%m-%d %H:%M:%S')
    today = datetime.today()
    days = timedelta(days=2)
    start_date, end_date = (today - days), today
    filterByDate = dados.loc[(dados['date'] >= start_date) & (dados['username'] == user)].sort_values(by=["date"], ascending=False).head(2)
    print(filterByDate)
    # comparando os seguidores
    filterSeguidores = list(filterByDate.listaSeguidores)
    diffListaSeguidores = set(filterSeguidores[0]) - set(filterSeguidores[1])
    # comparando os seguindo
    filterSeguindo = list(filterByDate.listaSeguindo)
    diffListaSeguindo = set(filterSeguindo[0]) - set(filterSeguindo[1])

    dadosLista = filterByDate.to_dict(orient='records')
    novosSeguindo = dadosLista[0]['qntSeguindo'] > dadosLista[1]['qntSeguindo']
    novosSeguidores = dadosLista[0]['qntSeguidores'] > dadosLista[1]['qntSeguidores']

    send(diffListaSeguidores, diffListaSeguindo , novosSeguidores, novosSeguindo, user)
