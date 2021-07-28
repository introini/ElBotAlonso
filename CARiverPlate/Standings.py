import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import numpy as np
from CARiverPlate import Teams

def getStandings(url):
    '''
    Creats a standings DataFrame with teams and stats 
    '''

    df = pd.read_html(url)
    teamNames = Teams.getShortNames(Teams.getTeams(url))
    teams = pd.DataFrame(teamNames, columns=['Equipo'])
    stats = df[1]
    table = pd.concat([teams, stats], axis=1)
    
    return table

def formatTable(table):
    '''
    Formats the table to remove unwanted columns. Also reorders
    the PTS column so that it appears after the team name.
    '''
    table.index = table.index + 1
    table.index.name = '#'
    table = table.drop(['GF','GC','E'], axis=1)
    cols = ['Equipo','PTS','J','G','DIF']
    table = table[cols]
    return table.to_markdown(numalign='center')