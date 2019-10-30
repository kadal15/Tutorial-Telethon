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