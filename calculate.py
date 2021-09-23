import pandas as pd
from dotenv import dotenv_values
from datetime import datetime, timedelta
from sendEmail import send
config = dotenv_values(".env")
usersSpy = config["SPY_ACCOUNTS"].split(',')
dados = pd.read_json("data/dados.json", orient='table')
def winOrLose(now, ago):
    return now - ago
def diffUsers(count, registerNow, registerAgo):
    if count > 0:
       return set(registerNow) - set(registerAgo)
    elif count < 0:
       return set(registerAgo) - set(registerNow)
    return 0
    
for user in usersSpy:
    dados['date'] = pd.to_datetime(dados.date, format='%Y-%m-%d %H:%M:%S')
    today = datetime.today()
    days = timedelta(days=2)
    start_date, end_date = (today - days), today
    filterByDate = dados.loc[(dados['date'] >= start_date) & (dados['username'] == user)].sort_values(by=["date"], ascending=False).head(2).reset_index()

    # comparando os seguidores

    changeFollowins = winOrLose(filterByDate.iloc[0].qntSeguindo, filterByDate.iloc[1].qntSeguindo)
    changeFollowers = winOrLose(filterByDate.iloc[0].qntSeguidores, filterByDate.iloc[1].qntSeguidores)

    diffListaSeguidores = diffUsers(changeFollowers, filterByDate.iloc[0].listaSeguidores, filterByDate.iloc[1].listaSeguidores)
    diffListaSeguindo = diffUsers(changeFollowins, filterByDate.iloc[0].listaSeguindo, filterByDate.iloc[1].listaSeguindo)

    send(diffListaSeguidores, diffListaSeguindo , changeFollowers, changeFollowins, user)
