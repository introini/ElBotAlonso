import logging
from bs4 import BeautifulSoup as bs
import requests
import re

from CARiverPlate import Config

def get_teams(url):
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


def get_short_names(teams):
    '''
    Clean up the long names from the list to fit in the matkdown table
    '''
    logger = Config.logger(__name__)
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

    for i,t in enumerate(teams):
        if t in shortNames:
            teams[i] = shortNames[t]
    logging.info(teams)
    return teams        