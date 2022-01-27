"""Update the River Plate subreddit"""
from pathlib import Path
import yaml
import praw
from CARiverPlate import Config, Fixture, Standings, UpdateSub

if __name__ == '__main__':
    config = Config.loadConf()

    nameToFile = {
        'Club Friendly': 'amistoso.png',
        'Liga Profesional de Argentina': 'lpf-2.png',
        'Copa Libertadores': 'libertadores-2.png',
        'Copa Argentina': "copa-argentina-2.png",
        'River Plate': 'riverplate.png',
        'Lanús': 'lanus.png',
        'Huracán': 'huracan.png',
        'Godoy Cruz Antonio Tomba': 'godoycruz.png',
        'Atlético-MG': 'atletico-mg.png',
        'Vélez Sarsfield': 'velez.png',
        'Gimnasia La Plata': 'gimnasia.png',
        'Aldosivi': 'aldosivi.png',
        'Sarmiento (Junín)': 'sarmiento.png',
        'Independiente': 'independiente.png',
        "Newell\'s Old Boys": "newells.png",
        'Arsenal de Sarandí': 'arsenal.png',
        'Central Córdoba (Santiago del Estero)': 'centralcordoba.png',
        'Boca Juniors': 'bocajuniors.png',
        'Banfield': 'banfield.png',
        'San Lorenzo': 'sanlorenzo.png',
        'Talleres (Córdoba)': 'talleres.png',
        'Argentinos Juniors': 'argentinos.png',
        'Estudiantes de La Plata': 'estudiantes.png',
        'Patronato': 'patronato.png',
        'Platense': 'platense.png',
        'Racing Club': 'racing.png',
        'Rosario Central': 'rosariocentral.png',
        'Defensa y Justicia': 'defensayjusticia.png',
        'Atlético Tucumán': 'atleticotucuman.png'
    }

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

    teams = Standings.get_standings(config['standingsURL'])
    table = Standings.format_table(teams)


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
    
    """ Don't update NGW before the game time """
    dates = Fixture.parse_date(ng['fecha'], ng['hora'])
    if dates[0] > dates[1]:
        UpdateSub.updateNextGameWidget(updateInfo, reddit, config['subreddit'])
