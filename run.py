import logging
from logger import Logger
logging.setLoggerClass(Logger)

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

from ocr import OCR
from ffr.ffr_core import FfrCore
from db_client import DbClient

client = discord.Client()


class DiscordBot():

    url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    post_channel_id = 672280665768591371

    logger = logging.getLogger('bot.discordBot')

    @staticmethod
    @client.event
    async def on_message(msg):
        # we do not want the bot to reply to itself
        if msg.author == client.user:
            return

        await DiscordBot.process_cmd(msg)
        await DiscordBot.process_attachments(msg)
        await DiscordBot.process_links(msg)
    

    @staticmethod
    @client.event
    async def on_ready():
        DiscordBot.logger.info('Bot ready')
        await client.change_presence(activity=discord.Game('Use me! Try .help'), status=discord.Status.online, afk=False)


    @staticmethod
    async def process_cmd(msg):
        if msg.content.startswith('.die'):
            DiscordBot.logger.info('Bot shutting down')
            await msg.channel.send('owh noe')
            exit(0)

        if msg.content.startswith('.help'):
            await msg.channel.send('TODO')

        if msg.content.startswith('.score'):
            pass


    @staticmethod
    async def process_attachments(msg):
        for attachment in msg.attachments:
            random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
            filename = f'tmp/{random_string}.jpg'

            try:
                with open(filename, 'wb') as f:
                    await attachment.save(f)

                await DiscordBot.process_image(msg, filename)

                os.remove(filename)

            except Exception as e:
                DiscordBot.logger.error(e)


    @staticmethod
    async def process_links(msg):
        urls = re.findall(DiscordBot.url_regex, msg.content)
        for url in urls:
            is_image_url = re.search(r"(?i)\.(jpe?g|png|gif)$", url[0])
            if is_image_url == None: return

            random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
            filename = f'tmp/{random_string}.{is_image_url.group(1)}'
            
            img_data = requests.get(url[0]).content
            with open(filename, 'wb') as handler:
                handler.write(img_data)

            await DiscordBot.process_image(msg, filename)                
            
            os.remove(filename)


    @staticmethod
    async def process_image(msg, filename):
        data = FfrCore(filename).process_image()
        if not DiscordBot.is_detection_valid(data['req'].values(), 0.6):
            DiscordBot.logger.info('Invalid detection')
            return

        channel = msg.channel
        #channel = client.get_channel(DiscordBot.post_channel_id)
        if channel: await DiscordBot.post(channel, data)
        else: DiscordBot.logger.info('Channel does not exit')

        DbClient.request_add_score(msg.author.id, data['req'])


    @staticmethod
    def is_detection_valid(values, threshold):
        '''
        If % of values that are not None exceeds 
        threshold, then the detection is valid
        '''
        num_not_none = sum([1 for value in values if value != None])
        return (num_not_none/len(values)) > threshold

        
    @staticmethod
    async def post(channel, data):
        text = ''.join([ f'{key}: {val}\n' for key, val in data['text'].items() ])
        await channel.send(text)

        for img in data['imgs']:
            random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
            filename = f'tmp/{random_string}.jpg'

            cv2.imwrite(filename, img) 
            with open(filename, 'rb') as f:
                if channel: await channel.send(file=discord.File(f))
                else: DiscordBot.logger.info('Channel does not exit')
            os.remove(filename)



if __name__ == '__main__':
    try: mkdir('tmp')
    except OSError as e:
        print('Unable to make directory named "tmp";', e)

    client.run(discord_token)