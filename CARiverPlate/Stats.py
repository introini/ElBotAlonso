import pandas as pd

def top_scorers(url, n=3):
    df = pd.read_html(url)
    goals = df[0][:n]
    goals.index += 1
    goals.index.name = '#'
    goals = goals.drop(['POS'], axis=1)
    goals = goals.to_markdown(numalign='center')
    
    return f'#### Goleadores\n{goals}'

def top_assists(url, n=3):
    df = pd.read_html(url)
    assists = df[1][:n]
    assists.index += 1
    assists.index.name = '#'
    assists = assists.drop(['POS'], axis=1)
    assists = assists.to_markdown(numalign='center')

    return f'#### Asistencias\n{assists}'
    