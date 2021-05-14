#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import requests

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2
import time
from PIL import Image, ImageDraw, ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
}
url='http://zndb.yxc.cn:8680/wxemcp/mine/balance'
data={
    'customerid':'34271',
}


try:

    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    # Drawing on the image
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font28 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 28)
    
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    epd.init(epd.PART_UPDATE)
    lastBalance=0.0
    while True:
        #epd.init(epd.FULL_UPDATE)
        #epd.Clear(0xFF)
        r = requests.post(url, data=data, headers=headers)
        ba=r.json()['data']['balance']
        uptime = "Update Time: \n" + str(time.ctime())
        balance = "Balance: " + str(ba)
        time_draw.rectangle((0, 0, 250, 122), fill = 255)
        time_draw.text((5, 10), uptime, font = font20, fill = 0)
        time_draw.text((5, 80), balance, font = font28, fill = 0)
        epd.displayPartial(epd.getbuffer(time_image))
        
        #draw.text((10,20), uptime, font=font20, fill=0)
        #draw.text((10,80),balance,font=font28,fill=0)
        #epd.display(epd.getbuffer(image))
        #print("Update Time: " + str(time.ctime()))
        #print("Balance: " + str(r.json()['data']['balance']))
        #time.sleep(3600*3)
        time.sleep(60*60*3)
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
