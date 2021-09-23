import pandas as pd
from dotenv import dotenv_values
from sendEmail import send

config = dotenv_values(".env")
usersSpy = config["SPY_ACCOUNTS"].split(',')
data = pd.read_json("data/dados.json", orient='table')

def winOrLose(now, ago):
    return now - ago
def diffUsers(count, registerNow, registerAgo):
    if count > 0:
       return set(registerNow) - set(registerAgo)
    elif count < 0:
       return set(registerAgo) - set(registerNow)
    return 0
    
for user in usersSpy:
    data['date'] = pd.to_datetime(data.date, format='%Y-%m-%d %H:%M:%S')
    filterByDate = data.loc[(data['username'] == user)].sort_values(by=["date"], ascending=False).head(2).reset_index()

    # comparando os seguidores

    changeFollowins = winOrLose(filterByDate.iloc[0].numberFollowins, filterByDate.iloc[1].numberFollowins)
    changeFollowers = winOrLose(filterByDate.iloc[0].numberFollowers, filterByDate.iloc[1].numberFollowers)

    diffListFollowers = diffUsers(changeFollowers, filterByDate.iloc[0].listFollowers, filterByDate.iloc[1].listFollowers)
    diffListFollowins = diffUsers(changeFollowins, filterByDate.iloc[0].listFollowins, filterByDate.iloc[1].listFollowins)

    send(diffListFollowers, diffListFollowins, changeFollowers, changeFollowins, user)
