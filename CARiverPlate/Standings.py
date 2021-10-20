"""Return a markdown table of team positions"""
import pandas as pd
from CARiverPlate import Teams

def get_standings(url):
    """Creats a standings DataFrame with teams and stats"""
    data_frame = pd.read_html(url)
    team_names = Teams.get_short_names(Teams.get_teams(url))
    teams = pd.DataFrame(team_names, columns=['Equipo'])
    stats = data_frame[1]
    table = pd.concat([teams, stats], axis=1)

    return table

def format_table(table):
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