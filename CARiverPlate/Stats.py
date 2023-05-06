import pandas as pd
from bs4 import BeautifulSoup as bs
import requests


def goal_stats_raw(url):
    req = requests.get(url)
    soup = bs(req.text, "lxml")
    table = soup.find_all("a", attrs={"class": "ListItem"})
    goals = []
    for item in table:
        player = (
            item.find("div", attrs={"class": "ListItem-text-value"})
            .find("div", attrs={"class": "ListItem-text"})
            .text
        )
        team = (
            item.find("div", attrs={"class": "ListItem-text-value"})
            .find("div", attrs={"class": "ListItem-value"})
            .text
        )
        stat = item.find("div", attrs={"class": "ListItem-meta"}).text
        goals.append((player, team, stat))

    return goals


def top_scorers(url, n=5):
    scorers = goal_stats_raw(url)
    df = pd.DataFrame(scorers, columns=["Jugador", "Equipo", "Goles"])
    goals = df[:n]
    goals.index += 1
    goals.index.name = "#"
    goals = goals.to_markdown(numalign="center")

    return f"#### Goleadores\n{goals}"


def top_assists(url, n=3):
    df = pd.read_html(url)
    assists = df[1][:n]
    assists.index += 1
    assists.index.name = "#"
    assists = assists.drop(["POS"], axis=1)
    assists = assists.to_markdown(numalign="center")

    return f"#### Asistencias\n{assists}"
