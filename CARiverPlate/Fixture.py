from bs4 import BeautifulSoup
from unidecode import unidecode
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw
from CARiverPlate import Config
import requests
import pandas as pd
import pytz
import re
import locale


def get_crests(files):
    im1 = Image.open(files[0])
    im2 = Image.open(files[1])

    return im1, im2


def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    return soup


def parse_date(raw_date, raw_time):
    days_map = {
        "Lun": "Mon",
        "Mar": "Tue",
        "Mié": "Wed",
        "Jue": "Thu",
        "Vie": "Fri",
        "Sáb": "Sat",
        "Dom": "Sun",
    }

    month_map = {
        "Ene": "Jan",
        "Feb": "Feb",
        "Mar": "Mar",
        "Abr": "Apr",
        "May": "May",
        "Jun": "Jun",
        "Jul": "Jul",
        "Ago": "Aug",
        "Sep": "Sep",
        "Oct": "Oct",
        "Nov": "Nov",
        "Dic": "Dec",
    }

    # Remove comma and dot characters from the date string
    raw_date = raw_date.replace(",", "").replace(".", "")

    # Map the day of the week abbreviation to its full name
    day_of_the_week = days_map[raw_date[:3]]

    # Get the day and month from the date string
    day = int(raw_date[4:6])
    month = month_map[raw_date[-3:]]

    # Get the current year
    year = datetime.today().year

    # Combine the date and time strings into a single string
    date_time_string = f"{day_of_the_week} {day} {month} {year}"
    # Parse the date and time string into a datetime object
    fixture_date = datetime.strptime(date_time_string, "%a %d %b %Y")
    if not pd.isnull(raw_time):
        fixture_datetime = datetime.combine(fixture_date, raw_time)
        return fixture_datetime


def strip_parentheses(s):
    return re.sub(r"\(|\)", "", s)


def get_match_links(soup):
    links = {}
    fixtures = soup.find_all("span", class_="Table__Team score")
    for fixture in fixtures:
        home = fixture.contents[0]["href"].split("/")[-1]
        match_link = f"https://espn.com.ar{fixture.contents[1]['href']}"
        away = fixture.contents[2]["href"].split("/")[-1]
        game_id = match_link.split("/")[-1]
        if game_id is not None and game_id not in links:
            links[(home, away)] = match_link

    return links


def format_fixture(df, links):
    # Rename columns
    df = df.rename(
        columns={
            "FECHA": "date",
            "Partido": "home",
            "Partido.2": "away",
            "HORA": "time_mia",
            "COMPETENCIA": "tournament",
        }
    )
    df["time_mia"] = pd.to_datetime(
        df["time_mia"], format="%I:%M %p", errors="coerce"
    ).dt.time
    df["datetime"] = df.apply(lambda x: parse_date(x.date, x.time_mia), axis=1)

    # Convert time to Buenos Aires timezone
    ar_tz = pytz.timezone("America/Argentina/Buenos_Aires")
    df["time_ba"] = df["datetime"]
    df.loc[df["time_ba"].apply(lambda x: x == pd.NaT), "time_ba"] = pd.NaT
    time_mask = df["time_ba"].apply(lambda x: not pd.isnull(x))
    df.loc[time_mask, "time_ba"] = df.loc[time_mask].apply(
        lambda row: pd.Timestamp.combine(row["datetime"].date(), row["time_ba"].time())
        .tz_localize(pytz.timezone("America/New_York"))
        .astimezone(ar_tz)
        .time(),
        axis=1,
    )

    df = df.drop(["TV", "Partido.1"], axis=1)

    # Format home and away columns
    df["home-slug"] = (
        df["home"].apply(strip_parentheses).str.lower().str.replace(" ", "-")
    )
    df["away-slug"] = (
        df["away"].apply(strip_parentheses).str.lower().str.replace(" ", "-")
    )

    # Strip accents from home and away columns
    df["home-slug"] = df["home-slug"].apply(unidecode)
    df["away-slug"] = df["away-slug"].apply(unidecode)

    # Create link column in DataFrame
    df["link"] = [
        links.get((row["home-slug"], row["away-slug"]), pd.NA)
        for _, row in df.iterrows()
    ]

    return df


def get_fixtures(url):
    links = get_match_links(get_soup(url))
    df = pd.read_html(url)
    df = df[0]
    return format_fixture(df, links)


def get_next_fixture(fixtures_df):
    logger = Config.logger(__name__)

    fixture_info = fixtures_df.iloc[0]

    next_fixture = {
        "fixture": fixture_info["datetime"],
        "time_mia": fixture_info["time_mia"],
        "time_ba": fixture_info["time_ba"],
        "home": fixture_info["home"],
        "away": fixture_info["away"],
        "tournament": fixture_info["tournament"],
    }

    logger.info(f"{next_fixture}")

    return next_fixture


def draw_text(img, text, font_type, font_size, font_color, offset=20, sections=2):
    # Draw the text on the image
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        font_type, font_size
    )  # Replace 'arial.ttf' with your font file path
    w, h = draw.textsize(text, font=font)
    if offset > 20:
        draw.text(
            (
                sum([(img.width - w) // 2, sections]),
                ((img.height - h) // 2) + offset + h,
            ),
            text,
            font=font,
            fill=font_color,
        )
    else:
        draw.text(
            (sum([(img.width - w) // 2, sections]), ((img.height - h) // 2) + offset),
            text,
            font=font,
            fill=font_color,
        )  # Change fill color if you like


def add_text_to_image(image, text, position, font_size, font_type, font_color):
    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Set the font
    font = ImageFont.truetype(font_type, font_size)

    # Calculate the position of the text relative to the image
    text_width, text_height = draw.textsize(text, font=font)
    text_x = int((image.width - text_width) * position[0])
    text_y = int((image.height - text_height) * position[1])

    # Add the text to the image
    draw.text((text_x, text_y), text, font_color, font=font)

    # Return the modified image
    return image


def make_image(info):
    logger = Config.logger(__name__)

    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

    W, H = (800, 600)
    crestSize = (300, 300)

    img = Image.new(mode="RGBA", size=(W, H), color=(34, 34, 34))
    images = get_crests([info["home"], info["away"]])

    for i, img_src in enumerate(images):
        img_crest = img_src.resize(crestSize)
        pos_x = 20 if i == 0 else (W - img_crest.size[0]) - 20
        img.paste(img_crest, (pos_x, 30), img_crest)

    times = f"{info['time_mia'].strftime('%I:%M %p')} / {info['time_ba'].strftime('%I:%M %p')}"

    add_text_to_image(
        img,
        info["fixture"].strftime("%a %d, %b").title(),
        (0.5, 0.7),
        69,
        info["font"],
        info["font_color"],
    )
    add_text_to_image(img, times, (0.5, 0.83), 40, info["font"], info["font_color"])
    add_text_to_image(img, "MIA", (0.28, 0.825), 26, info["font"], (190, 190, 190))
    add_text_to_image(img, "BUE", (0.72, 0.825), 26, info["font"], (190, 190, 190))

    tournament = Image.open(info["tournament"])
    tournament_img = tournament.resize(
        (tournament.size[0] // 5, tournament.size[1] // 5)
    )
    tournament_x = int((W - tournament_img.size[0]) * 0.5)
    tournament_y = int((H - tournament_img.size[1]) * 0.4)
    img.paste(tournament_img, (tournament_x, tournament_y), tournament_img)

    locale.setlocale(locale.LC_TIME, "en_US.UTF-8")

    file_name = f"{info['fileToUpload']}"
    img.save(file_name, "PNG")
    logger.info(f"{file_name} saved.")

    return file_name
