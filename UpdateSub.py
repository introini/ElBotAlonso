import yaml
import praw
from pathlib import Path
from CARiverPlate import Standings, Fixture, Config



def updateStandingsWidget(standings, subreddit):

    widgets = reddit.subreddit(subreddit).widgets
    for widget in widgets.sidebar:
        if widget.shortName == 'Liga Profesional':
            widget.mod.update(shortName="Liga Profesional", text=standings)
            widgets.refresh()

def updateNextGameWidget(updateInfo, subreddit):

    widgets = reddit.subreddit(subreddit).widgets
    for widget in widgets.sidebar:
        if widget.shortName == 'Próximo Partido':
            image_url = widgets.mod.upload_image(updateInfo['filePath'])
            image_data = [{'width': 800, 'height': 600, 'linkUrl': '', 'url': image_url}]
            widget.mod.update(data=image_data)
            widgets.refresh()

if __name__ == '__main__':

    config = Config.loadConf()

    nameToFile = {
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

    ng = Fixture.getNextGame(config['fixtureURL'])
    ng = {**ng, **config} # combine config and info from web into a single dict

    if nameToFile[ng['local']] is not None:
        ng['local'] = Path("escudos/{}".format(nameToFile[ng['local']])).resolve()

    if nameToFile[ng['visitante']] is not None:
        ng['visitante'] = Path("escudos/{}".format(nameToFile[ng['visitante']])).resolve()

    if nameToFile[ng['competencia']] is not None:
        ng['competencia'] = Path("escudos/{}".format(nameToFile[ng['competencia']])).resolve()


    fixtureFilePath = Path("{}".format(Fixture.makeImage(ng))).resolve()
    updateInfo = {'filePath': str(fixtureFilePath)}

    teams = Standings.getStandings(config['standingsURL'])
    table = Standings.formatTable(teams)


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

    updateStandingsWidget(table, config['subreddit'])
    updateNextGameWidget(updateInfo, config['subreddit'])