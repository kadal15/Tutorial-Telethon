from telethon import TelegramClient, sync, events
from telethon.tl.functions.messages import GetHistoryRequest, GetBotCallbackAnswerRequest
from telethon.errors import SessionPasswordNeededError
from time import sleep
import os

if not os.path.exists('session'):
    os.makedirs('session')


api_id = 837558
api_hash = 'e8832de14f7d085b075e195edf516f32'
phone_number = '+6285336117892'


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
print(myself.username)

channel_username = '@ClaimFreeBTCBot'
channel_entity = client.get_entity(channel_username)

while True:
    try:
        client.send_message(entity=channel_entity,message='🎁 Free bitcoin')
        sleep(3)
        message_history = client(GetHistoryRequest(peer=channel_entity,limit=1,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
        channel_id = message_history.messages[0].id
        client(GetBotCallbackAnswerRequest(channel_username,channel_id,data=message_history.messages[0].reply_markup.rows[0].buttons[0].data))
        sleep(3)
        message_history = client(GetHistoryRequest(peer=channel_entity,limit=1,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
        print(message_history)
    except:
        pass
    sleep(3600)