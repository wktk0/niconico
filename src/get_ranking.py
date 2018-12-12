import pandas as pd
import requests
import xmltodict
from bs4 import BeautifulSoup

from PIL import Image, ImageDraw, ImageFont

font =  ImageFont.truetype("/System/Library/Fonts/ヒラギノ明朝 ProN.ttc",15)

xml=requests.get("http://www.nicovideo.jp/ranking/fav/hourly/all?rss=2.0").text
dict=xmltodict.parse(xml)

for rank in range(0,10):
    title = dict["rss"]["channel"]["item"][rank]["title"]
    description=dict["rss"]["channel"]["item"][rank]["description"]
    soup = BeautifulSoup(description, "lxml")
    try:
        img_path = soup.findAll('img')[0]["src"]+".L"
        file =io.BytesIO(urllib.request.urlopen(img_path).read())
        img = Image.open(file)
    except:
        img_path = soup.findAll('img')[0]["src"]
        file =io.BytesIO(urllib.request.urlopen(img_path).read())
        img = Image.open(file)
        img = img.resize((360,270))
    #print(img_path)
    
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), title, fill=(255, 255, 255), font=font)
    img.save("thumbnail/{}.png".format(rank+1))
