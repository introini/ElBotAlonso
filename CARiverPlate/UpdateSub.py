from CARiverPlate import Standings, Fixture, Config


def updateStandingsWidget(standings, connection, subreddit):

    logger = Config.logger(__name__)
    widgets = connection.subreddit(subreddit).widgets
    for widget in widgets.sidebar:
        if widget.shortName == 'Copa Liga Profesional':
            widget.mod.update(shortName="Copa Liga Profesional", text=standings)
            widgets.refresh()
            logger.info(f'[{widget.shortName}] Updated latest standings table')

def updateNextGameWidget(updateInfo, connection, subreddit):

    logger = Config.logger(__name__)
    widgets = connection.subreddit(subreddit).widgets
    for widget in widgets.sidebar:
        if widget.shortName == 'Próximo Partido':
            image_url = widgets.mod.upload_image(updateInfo['filePath'])
            image_data = [{'width': 800, 'height': 600, 'linkUrl': '', 'url': image_url}]
            widget.mod.update(data=image_data)
            widgets.refresh()
            logger.info(f'[{widget.shortName}] Updated next game image')

def update_stats(stats, connection, subreddit):

    logger = Config.logger(__name__)
    widgets = connection.subreddit(subreddit).widgets
    for widget in widgets.sidebar:
        if widget.shortName == 'Estadísticas':
            widget.mod.update(shortName="Estadísticas", text=stats)
            widgets.refresh()
            logger.info(f'[{widget.shortName}] Updated stats')
