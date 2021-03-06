# /usr/bin/env python3.7
# -*- coding: utf-8 -*-
import datetime
from peewee import PrimaryKeyField, ForeignKeyField, DateTimeField, TextField
from models.BaseModel import BaseModel
from models.User import User, try_user
from models.Chat import Chat, try_chat


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


def add_text(user, chat, msg, attach):
    print(msg)

    row = Texts(
        id_user=user,
        id_chat=chat,
        text=msg,
        attach=attach
    )
    row.save(force_insert=True)
