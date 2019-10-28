from telethon import TelegramClient, sync, events
from telethon.tl.functions.messages import GetHistoryRequest, GetBotCallbackAnswerRequest
from telethon.errors import SessionPasswordNeededError
from bs4 import BeautifulSoup
from time import sleep
import requests, json, re, sys, os

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
print(myself)

channel_username = '@Dogecoin_click_bot'


c = requests.session()

ua = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}

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

    r = c.get(url,headers=ua)
    soup = BeautifulSoup(r.text,"html.parser")

    if soup.find('div',class_='g-recaptcha') is None and soup.find('div',id='headbar') is None:
        sleep(2)
        message_history = client(GetHistoryRequest(peer=channel_entity,limit=1,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
        message = message_history.messages[0].message
        print (message)
        if message_history.messages[0].message.find('Please stay on') != -1 or message_history.messages[0].message.find('You must stay') != -1:
            timer = re.findall(r'([\d.]*\d+)',message)
            sleep(int(timer[0]))
            sleep(3)
            message_history = client(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0,add_offset=0, hash=0))
            print(message_history.messages[0].message)

    elif soup.find('div',id='headbar') is not None:
        for data in soup.find_all('div',class_='container-fluid'):
            code = data.get('data-code')
            timer = data.get('data-timer')
            token = data.get('data-token')
            sleep(int(timer))
            r = c.post('https://dogeclick.com/reward',data={'code': code, 'token': token},headers=ua)
            jsn = json.loads(r.text)
            print ("You earned "+jsn['reward']+" Doge for visiting sites")
    else:
        print ('Captcha detected')
        client(GetBotCallbackAnswerRequest(channel_username,channel_id,data=message_history.messages[0].reply_markup.rows[1].buttons[1].data))
        print ('Berhasil Skip Captcha')




