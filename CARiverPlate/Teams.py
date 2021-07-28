import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import numpy as np
import re

def getTeams(url):
    '''
    Gets a list of teams from the ESPN website and returns a list with
    shortend a version of each team name.
    '''
    teams = []
    req = requests.get(url)
    soup = bs(req.text, 'lxml')
    for child in soup.find_all('table')[0].children:
        for td in child:
            for i in td.find_all(class_='hide-mobile'):
                team = re.sub(r'\(([^\)]+)\)', '', i.text)
                team = team.strip()
                teams.append(team)
    return teams


def getShortNames(teams):

    shortNames = {
        'Estudiantes de La Plata': 'Estudiantes',
        'Godoy Cruz Antonio Tomba': 'Godoy Cruz',
        'Newell\'s Old Boys': 'Newell\'s',
        'Gimnasia La Plata': 'Gimnasia',
        'Arsenal de Sarandí': 'Arsenal',
        'Argentinos Juniors': 'Argentinos Jrs',
        'Boca Juniors': 'Boca Jrs',
        'Central Córdoba': 'Central Cba',
        'Vélez Sarsfield': 'Vélez',
        'River Plate': '**River Plate**'
    }

    shortendList = []

    for i,t in enumerate(teams):
        if t in shortNames:
            teams[i] = shortNames[t]

    return teams        