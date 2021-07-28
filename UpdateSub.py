import yaml
import praw
from CARiverPlate import Standings, Fixture


def updateStandingsWidget(standings):
    config = yaml.load(open('keys.yml', 'r'), Loader=yaml.FullLoader)
    reddit = praw.Reddit(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        user_agent=config['user_agent'],
        username=config['username'],
        password=config['password']
    )

    widgets = reddit.subreddit(config['subreddit']).widgets
    for widget in widgets.sidebar:
        if widget.shortName == 'Liga Profesional':
            widget.mod.update(shortName="Liga Profesional", text=standings)
            widgets.refresh()

def updateNextGameWidget(updateInfo):
    config = yaml.load(open('keys.yml', 'r'), Loader=yaml.FullLoader)
    reddit = praw.Reddit(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        user_agent=config['user_agent'],
        username=config['username'],
        password=config['password']
    )

    widgets = reddit.subreddit(config['subreddit']).widgets
    for widget in widgets.sidebar:
        if widget.shortName == 'Próximo Partido':
            image_url = widgets.mod.upload_image(updateInfo['filePath'])
            image_data = [{'width': 800, 'height': 600, 'linkUrl': '', 'url': image_url}]
            widget.mod.update(data=image_data)
            widgets.refresh()

if __name__ == '__main__':
    standingsURL = "https://espndeportes.espn.com/futbol/posiciones/_/liga/arg.1" 
    fixtureURL = "https://espndeportes.espn.com/futbol/equipo/calendario/_/id/16/river-plate"
    nameToFile = {
        'Liga Profesional de Argentina': 'lpf-2.png',
        'Copa Libertadores': 'libertadores-2.png',
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

    ng = Fixture.getNextGame(fixtureURL)

    if nameToFile[ng['local']] is not None:
        ng['local'] = "./escudos/{}".format(nameToFile[ng['local']])

    if nameToFile[ng['visitante']] is not None:
        ng['visitante'] = "./escudos/{}".format(nameToFile[ng['visitante']])

    if nameToFile[ng['competencia']] is not None:
        ng['competencia'] = "./escudos/{}".format(nameToFile[ng['competencia']])


    fixtureFilePath = "./{}".format(Fixture.makeImage(ng))
    updateInfo = {'filePath': fixtureFilePath}

    teams = Standings.getStandings(standingsURL)
    table = Standings.formatTable(teams)
    updateStandingsWidget(table)
    updateNextGameWidget(updateInfo)