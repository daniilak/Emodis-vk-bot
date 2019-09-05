# /usr/bin/env python3.7
# -*- coding: utf-8 -*-

import vk
import peewee
from random import randint
from requests import post
from config import VK_API_ACCESS_TOKEN, VK_API_VERSION, GROUP_ID
from lib.DataBase import DataBase, IntegrityError, OperationalError
from lib.Controller import Controller
from models.Chat import find_chat

api = vk.API(vk.Session(access_token=VK_API_ACCESS_TOKEN), v=VK_API_VERSION)
controller = Controller()
db = DataBase()
longPoll = api.groups.getLongPollServer(group_id=GROUP_ID)
server, key, ts = longPoll['server'], longPoll['key'], longPoll['ts']

while True:
    try:
        try:
            db.open_connection()
        except (peewee.OperationalError):
            print("connection")
    except (IntegrityError, OperationalError):
        db = DataBase()
        db.open_connection()

    print("new LongPoll post request")
    longPoll = post('%s' % server, data={'act': 'a_check',
                                         'key': key,
                                         'ts': ts,
                                         'wait': 25}).json()

    if longPoll.get('updates') and len(longPoll['updates']) != 0:
        for update in longPoll['updates']:
            chat = find_chat(int(update['object']['peer_id']) - 2000000000)
            user = controller.update_user(update['object']['from_id'])
            controller.update_temp_data(chat, user, update['object'])

            if update['object'].get('action'):
                controller.action_parser(update['object']['action'])
            else:
                controller.update_user_stats()
                controller.add_text()
                controller.get_reaction()
                # дальше реальный Коммандхендлер
                controller.is_mini_request_for_reply()
                if controller.is_request_bot():
                    controller.parse_command()
                controller.duel()
    db.close_connection()
    if longPoll.get('failed'):
        longPoll = api.groups.getLongPollServer(group_id=GROUP_ID)
        server, key, ts = longPoll['server'], longPoll['key'], longPoll['ts']
    ts = longPoll['ts']
