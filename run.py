import logging
from logger import Logger
logging.setLoggerClass(Logger)

import importlib
import datetime
import requests
import discord
import string
import random
import time
import cv2
import re
import os

from config import discord_token
from utils import mkdir

from cmd_core import Cmd
from cmd_proc import CmdProc

from evalscreen_ocr.ffr.ffr_core import FfrCore
from db_client import DbClient


client = discord.Client()


class DiscordBot(discord.AutoShardedClient):
    """
    Discord bot


    """

    url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    post_channel_id = 672280665768591371


    def __init__(self):
        super().__init__()

        self.logger = logging.getLogger('bot.discordBot')

        CmdProc.init()
        super().run(discord_token)


    @client.event
    async def on_message(self, msg):
        # we do not want the bot to reply to itself
        if msg.author == client.user:
            return

        if (cmd_data := CmdProc.parse_cmd(msg.content)) != None:
            ret = await CmdProc.exec_cmd(cmd_data, msg)
            if ret['status'] == -1:
                await msg.channel.send(ret['msg'])

        await self.process_attachments(msg)
        await self.process_links(msg)
    

    @client.event
    async def on_ready(self):
        self.logger.info('Bot ready')
        await self.change_presence(activity=discord.Game('Use me! Try >>help'), status=discord.Status.online, afk=False)


    async def process_attachments(self, msg):
        for attachment in msg.attachments:
            random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
            filename = f'tmp/{random_string}.jpg'

            try:
                with open(filename, 'wb') as f:
                    await attachment.save(f)

                await self.process_image(msg, filename)

                os.remove(filename)

            except Exception as e:
                self.logger.error(e)


    async def process_links(self, msg):
        urls = re.findall(self.url_regex, msg.content)
        for url in urls:
            is_image_url = re.search(r"(?i)\.(jpe?g|png|gif)$", url[0])
            if is_image_url == None: return

            random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
            filename = f'tmp/{random_string}.{is_image_url.group(1)}'
            
            img_data = requests.get(url[0]).content
            with open(filename, 'wb') as handler:
                handler.write(img_data)

            await self.process_image(msg, filename)                
            
            os.remove(filename)


    async def process_image(self, msg, filename):
        img_data, txt_data = FfrCore(filename).process()
        
        if not self.is_detection_valid(txt_data.values(), 0.6):
            self.logger.info('Invalid detection')
            return

        channel = msg.channel
        #channel = client.get_channel(self.post_channel_id)
        if channel: await self.post(channel, txt_data, img_data)
        else: self.logger.info('Channel does not exit')

        DbClient.request(DbClient.REQUEST_ADD_SCORE, msg.author.id, self.data_convert(txt_data))


    def is_detection_valid(self, values, threshold):
        '''
        If % of values that are not None exceeds 
        threshold, then the detection is valid
        '''
        num_not_none = sum([1 for value in values if value != None])
        return (num_not_none/len(values)) > threshold

        
    async def post(self, channel, txt_data, img_data):
        # Post detected text data to channel
        text = ''.join([ f'{key}: {val}\n' for key, val in txt_data.items() ])
        await channel.send(text)

        # Post processed image data to channel
        for img in img_data.values():
            random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
            filename = f'tmp/{random_string}.jpg'

            cv2.imwrite(filename, img) 
            with open(filename, 'rb') as f:
                if channel: await channel.send(file=discord.File(f))
                else: self.logger.info('Channel does not exit')
            os.remove(filename)


    def data_convert(self, txt_data):
        req_data = {}

        try:
            req_data['date'] = datetime.datetime(
                int(txt_data['year']), 
                int(txt_data['month']), 
                int(txt_data['day']), 
                int(txt_data['hour'] + 12 if txt_data['ampm'] == 'pm' else txt_data['hour']),
                int(txt_data['minute']),
                int(txt_data['second'])).timestamp()
        except TypeError as e:
            self.logger.info(f'Unable to process score datetime; {e}')

        req_data['player']  = str(txt_data['player'])
        req_data['title']   = str(txt_data['title'])
        req_data['artist']  = str(txt_data['artist'])
        req_data['creator'] = str(txt_data['creator'])

        try:
            req_data['combo'] = int(txt_data['combo'])
            req_data['w0']    = int(txt_data['amazing_score'])
            req_data['w1']    = int(txt_data['perfect_score'])
            req_data['w2']    = int(txt_data['good_score'])
            req_data['w3']    = int(txt_data['average_score'])
            req_data['w4']    = int(txt_data['miss_score'])
            req_data['w5']    = int(txt_data['boo_score'])
            req_data['equiv'] = float(txt_data['AAA_equiv'])
            req_data['raw']   = float(txt_data['raw_goods'])
        except TypeError as e:
            self.logger.info(f'Unable to process score data; {e}')

        return req_data



if __name__ == '__main__':
    try: mkdir('tmp')
    except OSError as e:
        print('Unable to make directory named "tmp";', e)

    bot = DiscordBot()