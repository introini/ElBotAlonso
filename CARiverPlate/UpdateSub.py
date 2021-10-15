from CARiverPlate import Standings, Fixture, Config


def updateStandingsWidget(standings, connection, subreddit):
    config = Config.loadConf()

    logger = Config.logger()
    widgets = connection.subreddit(subreddit).widgets
    for widget in widgets.sidebar:
        if widget.shortName == 'Liga Profesional':
            widget.mod.update(shortName="Liga Profesional", text=standings)
            widgets.refresh()
            logger.info(f'[{widget.shortName}] Updated latest standings table')

def updateNextGameWidget(updateInfo, connection, subreddit):

    logger = Config.logger()
    widgets = connection.subreddit(subreddit).widgets
    for widget in widgets.sidebar:
        if widget.shortName == 'Próximo Partido':
            image_url = widgets.mod.upload_image(updateInfo['filePath'])
            image_data = [{'width': 800, 'height': 600, 'linkUrl': '', 'url': image_url}]
            widget.mod.update(data=image_data)
            widgets.refresh()
            logger.info(f'[{widget.shortName}] Updated next game image')
