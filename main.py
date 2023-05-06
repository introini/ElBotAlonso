"""Update the River Plate subreddit"""
import datetime
from pathlib import Path
import yaml
import praw
from CARiverPlate import Config, Standings, Stats, UpdateSub, Fixture

if __name__ == "__main__":
    config = Config.loadConf()
    nameToFile = config["name_to_file"]

    fixtues = Fixture.get_fixtures(config["fixtureURL"])
    ng = Fixture.get_next_fixture(fixtues)
    ng = {**ng, **config}  # combine config and info from web into a single dict

    if nameToFile[ng["home"]] is not None:
        ng["home"] = Path("escudos/{}".format(nameToFile[ng["home"]])).resolve()

    if nameToFile[ng["away"]] is not None:
        ng["away"] = Path("escudos/{}".format(nameToFile[ng["away"]])).resolve()

    if nameToFile[ng["tournament"]] is not None:
        ng["tournament"] = Path(
            "escudos/{}".format(nameToFile[ng["tournament"]])
        ).resolve()

    fixtureFilePath = Path("{}".format(Fixture.make_image(ng))).resolve()
    updateInfo = {"filePath": str(fixtureFilePath)}

    teams_table = Standings.get_standings(config["standingsURL"], groups=False)

    if len(teams_table) > 1:
        tableA = Standings.format_table(teams_table[0])
        tableB = Standings.format_table(teams_table[1])
        table = f"####Groupo A\n{tableA}\n\n####Groupo B\n{tableB}"
    else:
        table = Standings.format_table(teams_table[0])

    top_scorers = Stats.top_scorers(config["scorerStatsURL"])
    stats = f"{top_scorers}"

    """ Connect To Reddit and update the page """
    keyPath = Path("./keys.yml").resolve()
    secrets = yaml.safe_load(open(keyPath, "r"))
    reddit = praw.Reddit(
        client_id=secrets["client_id"],
        client_secret=secrets["client_secret"],
        user_agent=secrets["user_agent"],
        username=secrets["username"],
        password=secrets["password"],
    )

    UpdateSub.updateStandingsWidget(table, reddit, config["subreddit"])
    UpdateSub.update_stats(stats, reddit, config["subreddit"])
    """ Don't update NGW before the game time """

    dates = datetime.datetime.now(), ng["fixture"]
    if dates[0] > dates[1]:
        UpdateSub.updateNextGameWidget(updateInfo, reddit, config["subreddit"])
