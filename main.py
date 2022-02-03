"""Update the River Plate subreddit"""
from pathlib import Path
import yaml
import praw
from CARiverPlate import Config, Fixture, Standings, Stats, UpdateSub

if __name__ == '__main__':
    config = Config.loadConf()    
    nameToFile = config['name_to_file']

    ng = Fixture.get_next_game(config['fixtureURL'])
    ng = {**ng, **config} # combine config and info from web into a single dict

    if nameToFile[ng['local']] is not None:
        ng['local'] = Path("escudos/{}".format(nameToFile[ng['local']])).resolve()

    if nameToFile[ng['visitante']] is not None:
        ng['visitante'] = Path("escudos/{}".format(nameToFile[ng['visitante']])).resolve()

    if nameToFile[ng['competencia']] is not None:
        ng['competencia'] = Path("escudos/{}".format(nameToFile[ng['competencia']])).resolve()

    fixtureFilePath = Path("{}".format(Fixture.make_image(ng))).resolve()
    updateInfo = {'filePath': str(fixtureFilePath)}

    teams_table = Standings.get_standings(config['standingsURL'], groups=True)

    if len(teams_table) > 1:
        tableA = Standings.format_table(teams_table[0])
        tableB = Standings.format_table(teams_table[1])
        table = f"####Groupo A\n{tableA}\n\n####Groupo B\n{tableB}"
    else:  
        table = Standings.format_table(teams)
    
    top_scorers = Stats.top_scorers(config['scorerStatsURL'])
    top_assists = Stats.top_assists(config['scorerStatsURL'])
    stats = f'{top_scorers}\n{top_assists}\n'

    """ Connect To Reddit and update the page """
    keyPath = Path('./keys.yml').resolve()
    secrets = yaml.safe_load(open(keyPath, 'r'))
    reddit = praw.Reddit(
        client_id=secrets['client_id'],
        client_secret=secrets['client_secret'],
        user_agent=secrets['user_agent'],
        username=secrets['username'],
        password=secrets['password'],
    )

    UpdateSub.updateStandingsWidget(table, reddit, config['subreddit'])
    UpdateSub.update_stats(stats, reddit, config['subreddit'])
    """ Don't update NGW before the game time """
    dates = Fixture.parse_date(ng['fecha'], ng['hora'])
    if dates[0] > dates[1]:
        UpdateSub.updateNextGameWidget(updateInfo, reddit, config['subreddit'])
