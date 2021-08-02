from PIL import Image, ImageFont, ImageDraw
from CARiverPlate import Teams
import pandas as pd
from datetime import datetime
import pytz
from pathlib import Path
import re

def getCrests(files):
    size = 128, 128

    im1 = Image.open(files[0])
    im2 = Image.open(files[1])

    return (im1, im2)

def getNextGame(url):
    df = pd.read_html(url)
    nextGameRow = df[0].iloc[0]
    fecha = re.sub(r'\.,','',nextGameRow['FECHA']).strip('.')
    hora = nextGameRow['HORA']
    local = nextGameRow['Partido']
    visitante = nextGameRow['Partido.2']
    competencia = nextGameRow['COMPETENCIA']
    
    nextGame = {
        'fecha': fecha,
        'hora': hora,
        'competencia': competencia,
        'local': local,
        'visitante': visitante
    }
    
    return nextGame

def makeImage(info):
    W, H = (800, 600)
    fileName = "proximo-partido.png"
    zone_ny = pytz.timezone("America/New_York")
    crestSize = (275,275)
    where = ['MIA','BUE']

    img = Image.new(mode = "RGBA", size = (W,H), color=(34,34,34))

    images = getCrests([info['local'],info['visitante']]) 
    image1 = images[0].resize(crestSize)
    image2 = images[1].resize(crestSize)
    img.paste(image1, (20,20), image1)
    img.paste(image2, ((W-image2.size[0])-20,20), image2)
    
    offset = 20

    fecha = info['fecha']
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("NotoSansCJK-Regular.ttc", 69)
    w,h = draw.textsize(fecha, font=font)
    draw.text(((W-w)//2,((H-h)//2)+offset),fecha, font=font, fill="white")

    hora = pd.Timestamp(info['hora'])
    hora = zone_ny.localize(hora)
    hora_arg = hora.tz_convert(tz="America/Argentina/Buenos_Aires")
    hora_eeuu = hora.tz_convert(tz="America/New_York")

    hora_arg = str(hora_arg.strftime("%I:%M %p"))
    hora_eeuu  = str(hora_eeuu.strftime("%I:%M %p"))

    hora = "{} / {}".format(hora_eeuu, hora_arg)

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("NotoSansCJK-Regular.ttc", 40)
    hora_w,hora_h = draw.textsize(hora, font=font)
    draw.text(((W-hora_w)//2,((H-hora_h)//2)+offset+hora_h+10),hora, font=font, fill="white")

    font = ImageFont.truetype("NotoSansCJK-Regular.ttc", 22)
    w,h = draw.textsize(where[0])
    draw.text(((W-w)//2-220,((H-h)//2)+offset+hora_h+6), where[0], font=font, fill="white")

    font = ImageFont.truetype("NotoSansCJK-Regular.ttc", 22 )
    w,h = draw.textsize(where[1])
    draw.text(((W-w)//2+200,((H-h)//2)+offset+hora_h+6), where[1], font=font, fill="white")

    competencia = Image.open(info['competencia'])
    competenciaImg = competencia.resize((competencia.size[0]//6,competencia.size[1]//6))
    img.paste(competenciaImg, ((W-competenciaImg.size[0])//2,((H-competenciaImg.size[1])-28)), competenciaImg)

    img.save(fileName, "PNG")

    # img.show()

    return fileName