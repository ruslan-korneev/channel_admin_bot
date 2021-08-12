from pyrogram import Client, filters
from pyrogram.errors import FloodWait
 
from pyrogram.types import ChatPermissions
 
import os
import time
from time import sleep
import random


api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
 
app = Client("my_account", api_id, api_hash)


@app.on_message(filters.command("spam", prefixes="!"))
def spam_in_chat(_, msg):
    chat = msg.text.split()[1]
    amount = int(msg.text.split()[2])
    for i in range(amount):
        app.send_message(chat_id=chat, text="СПАМ")


@app.on_message(filters.command("del_memb", prefixes="!") & filters.me)
def delete_all_members(_, msg):
    chat = msg.text.split("!del_memb ", maxsplit=1)[1]
 
    members = [ x for x in app.iter_chat_members(chat) if x.status not in ("administrator", "creator") ]
 
    for i in range(len(members)):
        try:
            app.kick_chat_member(
                chat_id=chat,
                user_id=members[i].user.id)
        except FloodWait as e:
            print("> waiting", e.x, "seconds.")
            time.sleep(e.x)


@app.on_message(filters.command("del_mess", prefixes="!") & filters.me)
def delete_all_messages(_, msg):
    chat = msg.text.split("!del_mess", maxsplit=1)[1]
    messages = [message for message in app.iter_history(chat)]
    for message in messages:
        app.delete_messages(chat_id=chat, message_ids=message.message_id)

app.run()
