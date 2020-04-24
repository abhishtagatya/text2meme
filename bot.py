import re
import json
import requests
from datetime import datetime

from config import *

import discord
import joblib
import pymongo

class MemeAIBot(discord.Client):

    def __init__(self, filepath, credential, mongo_uri="mongodb://localhost:27017/"):
        super().__init__()
        self.prefix = '$$'
        self.credential = credential
        self.meme_clf = joblib.load(filepath['clf'])

        mongo_client = pymongo.MongoClient(mongo_uri)
        self.db = mongo_client["meme_ai"]

        with open(filepath['list'], 'r') as meme_list:
            self.meme_list = json.load(meme_list)

    async def on_ready(self):
        print('Logged As : {0.user.name} | {0.user.id}'.format(self))
        
    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith(self.prefix):
            [command] = re.findall('^([^\s]+)', message.content)
            message_clean = re.sub('^([^\s]+)', '', message.content)
            
            if command == '$$meme':
                resp, meme_class = self.generate_meme(message.author, message_clean)
                if resp['success']:
                    await message.channel.send(resp['data']['url'])
                else:
                    await message.channel.send('Meme Failed To Generate...')
                self.insert_text_to_db(message, meme_class, resp)
            elif command == '$$list':
                resp = self.generate_list_response()
                await message.channel.send(resp)
            elif command == '$$info':
                resp = self.generate_info_response(message_clean)
                await message.channel.send(resp)
            else:
                resp = self.generate_help_response()
                await message.channel.send(resp)

    def generate_help_response(self):
        resp_str = '**Bot Comands**\n\n>>> '
        resp_str += '`{0.prefix}meme` : generates meme from message\n'.format(self)
        resp_str += """```cs
example : '$meme text1, text2' | text boxes seperated by commas)```\n"""

        resp_str += '`{0.prefix}list` : return a list of generatable meme\n\n'.format(self)

        resp_str += '`{0.prefix}info` : return information of a meme number\n'.format(self)
        resp_str += """```cs
example : '$info 1'```\n"""
        return resp_str

    def generate_list_response(self):
        list_str = '**Available Meme List**\n\n>>> '
        for meme in self.meme_list:
            list_str += '`{0}` = {1}\n'.format(meme['id'], meme['meme_label'])
        return list_str

    def generate_info_response(self, message):
        resp = None
        meme_found = None

        for meme in self.meme_list:
            if str(meme['id']) == message.strip():
                meme_found = meme
        
        if meme_found:
            resp = """
            **{0}**
            >>> ```cs
Base Image   : '{1}'
Dimension    
    L Width  : {2}
    L Height : {3}
Text Boxes   : {4}
            ```""".format(
                meme_found['meme_label'],
                meme_found['base_img'],
                meme_found['dimension']['width'],
                meme_found['dimension']['height'],
                meme_found['dimension']['text_box']
            )
            return resp
        
        resp = "Oops... I didn't find any information on `{}`".format(message)
        return resp

    def insert_text_to_db(self, message, meme_class, resp):
        collection = self.db["bot_meme_message"]
        print(message.author)
        row = {
            "created_at" : datetime.now(),
            "message_id" : message.id,
            "message_author" : message.author.name,
            "message_content" : message.content,
            "classified_as" : meme_class,
            "generation_success" : resp['success'],
            "image_url" : resp['data']['url']
        }
        collection.insert_one(row)

    def generate_meme(self, user, message):

        # Split Message In To Boxes
        message_split = message.split(',')
        message_split = [message.strip().upper() for message in message_split]
        box_count = len(message_split)

        # Predict The Meme
        [meme_found] = self.meme_clf.predict([message])

        # Find The Meme In the List
        meme_ref = None
        for meme in self.meme_list:
            if meme['meme_label'] == meme_found:
                meme_ref = meme

        # Form a request to IMGFLIP
        body = {
            "template_id" : meme_ref['imgflip_id'],
            "username" : self.credential['username'],
            "password" : self.credential['password'],
        }
        for i, msg in enumerate(message_split):
            body["text"+str(i)] = msg
        resp = requests.post(self.credential['url'], body).json()

        return resp, meme_found

filepaths = {
    'clf' : './assets/meme_classifier.sav',
    'list' : './assets/memes_list.json'
}

creds = {
    "url" : IMGFLIP_URI,
    "username" : IMGFLIP_USER,
    "password" : IMGFLIP_PASS
}
client = MemeAIBot(filepaths, creds)
client.run(DISCORD_TOKEN)