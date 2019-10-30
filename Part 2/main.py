from telethon import TelegramClient, sync, events
from telethon.tl.functions.messages import GetHistoryRequest, GetBotCallbackAnswerRequest
from telethon.errors import SessionPasswordNeededError
from bs4 import BeautifulSoup
from time import sleep
import requests, json, re, sys, os

if not os.path.exists('session'):
    os.makedirs('session')

api_id = '<API ID>'
api_hash = '<API HASH>'
phone_number = '+6285xxxxxxxxx'

client = TelegramClient('session/'+phone_number,api_id,api_hash)
client.connect()
if not client.is_user_authorized():
    try:
        client.send_code_request(phone_number)
        me = client.sign_in(phone_number,input('Masukan Code Anda >> '))
    except SessionPasswordNeededError:
        password = input('Masukan Password 2fa Anda >> ')
        me = client.start(phone_number,password)

myself = client.get_me()
print(myself)

channel_username = '@Dogecoin_click_bot'
channel_entity = client.get_entity(channel_username)
for ulang in range(999999999):
    print ('Mencoba Mengambil URL')
    client.send_message(entity=channel_entity,message='🖥 Visit sites')
    sleep(3)
    message_history = client(GetHistoryRequest(peer=channel_entity,limit=1,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
    channel_id = message_history.messages[0].id
    if message_history.messages[0].message.find('Sorry, there are no new ads available.') != -1:
        print('Iklan SUdah Habis Silahkan Coba Lagi Nanti')
        break
    url = message_history.messages[0].reply_markup.rows[0].buttons[0].url
    print('Visit To URL '+url)