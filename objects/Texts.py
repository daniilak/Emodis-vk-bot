# /usr/bin/env python3.7
# -*- coding: utf-8 -*-
from peewee import *
from random import randint
import datetime
import peewee
import re
from objects.DataBase import *
from objects.User import *
from objects.Chat import *


class Texts(BaseModel):
    id = PrimaryKeyField(null=False)
    id_user = ForeignKeyField(User, db_column='id_user', related_name='fk_user',
                              to_field='id', on_delete='cascade', on_update='cascade')
    id_chat = ForeignKeyField(Chat, db_column='id_chat', related_name='fk_chat',
                              to_field='id', on_delete='cascade', on_update='cascade')
    text = TextField(null=False, default='')
    attach = TextField(null=False, default='')
    date_time = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "texts"
        order_by = ('id',)


def add_text(user_id, chat_id, msg, attach):
    user = try_user(user_id)
    chat = try_chat(chat_id)

    if user and chat:
        row = Texts(
            id_user=user,
            id_chat=chat,
            text=msg,
            attach=attach
        )
        row.save(force_insert=True)
