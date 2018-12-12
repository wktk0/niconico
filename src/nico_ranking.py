import io
import requests
import xmltodict
import urllib
import urllib.request
from bs4 import BeautifulSoup

from PIL import Image, ImageDraw, ImageFont
def nico_ranking(args,stdin):
    DISPLAY_NUM=30
    if (len(args))==0:
      category="all"
    elif args[0] in ["game","anime","jikkyo","toho","vocaloid","g_ent2","virtual","sing"]:
      category=args[0]
    else:
      category = "all"
    font =  ImageFont.truetype("/System/Library/Fonts/ヒラギノ明朝 ProN.ttc",15)

    xml=requests.get("http://www.nicovideo.jp/ranking/fav/hourly/{}?rss=2.0".format(category)).text
    dict=xmltodict.parse(xml)
    urls = []

    for rank in range(0,DISPLAY_NUM):
        title = dict["rss"]["channel"]["item"][rank]["title"]
        description=dict["rss"]["channel"]["item"][rank]["description"]
        url=dict["rss"]["channel"]["item"][rank]["link"]
        urls.append(url)
        soup = BeautifulSoup(description, "html.parser")
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
        img.save("/tmp/{}.png".format(rank+1))
        #plt.imshow(img)
        #plt.show()

    img = Image.new('RGB', (360 * 5, 270*DISPLAY_NUM//5))
    for j in range(DISPLAY_NUM):
        im = Image.open("/tmp/{}.png".format(j+1))
        #if j//5==1:
        img.paste(im, ( 360*((j%5)), 270*(j//5)))
        #else:
            #img.paste(im, ( 360*(j), 270*(j//5)))
    img.save("/tmp/h.png")
    imgcat /Users/gabdro/NICONICO/tmp/h.png
    
    img_num = input('image number(1~{}) : '.format(DISPLAY_NUM))
    try:
      echo -n @(urls[int(img_num)-1]) | pbcopy
    except:
      print('Bad input.')

aliases["niconico"] = nico_ranking
