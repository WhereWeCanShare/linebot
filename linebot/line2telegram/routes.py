from flask import Blueprint, request
import psycopg2
import os
import datetime
import requests
import logging

from linebot.settings import *

# get the key from system variables in .env
LINE_TOKEN = os.getenv('LINE_TOKEN')
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHANNEL = os.getenv('TG_CHANNEL')
TG_URL = f'https://api.telegram.org/bot{TG_TOKEN}/sendmessage'

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

## initial all variable
discard_events = ['join', 'leave', 'memberJoined', 'memberLeft', 'follow', 'unfollow', 'leave', 'postback', 'beacon', 'accountLink', 'things', ]
others_type = ['image', 'video', 'sticker', 'file']

logging.basicConfig(filename='l2tg.log', level=logging.DEBUG, format='')
logging.info(f'\n=== Service start {datetime.datetime.today()}')
print(f'\n=== Service start {datetime.datetime.today()}')

try:
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASS
    )
except:
    print(f'Unable to connect to DB')
else:
    print(f'Successful connect to db {DB_NAME}')
    conn.close()

l2tg = Blueprint('l2tg', __name__)

@l2tg.route('/', methods=['POST', 'GET'])
def l2tg_main():
    
    if request.method == 'POST':
        payload = request.json
    
        # logging to file.
        logging.info(f'\n--- Webhook {datetime.datetime.today()}')
        logging.info(payload)
        print(f'\n--- Webhook {datetime.datetime.today()}')
        print(payload)

        # discard some LINE events.
        if payload['events'][0]['type'] in discard_events:
            return '.l.', 200

        fwdmsg = ''

        # GROUP info
        if payload['events'][0]['source']['type'] == 'group':
            groupid = payload['events'][0]['source']['groupId']
            userid = payload['events'][0]['source']['userId']

            fwdmsg = get_user_name('group', groupid, userid) + ") in (" + get_group_name(groupid)

        # ROOM info
        if payload['events'][0]['source']['type'] == 'room':
            roomid = payload['events'][0]['source']['roomId']
            userid = payload['events'][0]['source']['userId']

            fwdmsg = get_user_name('room', roomid, userid) + ") in room."

        # check only text type will forward to Telegram
        if payload['events'][0]['message']['type'] == 'text':
            message = "LINE: (" + fwdmsg + ")\n\n"
            message += payload['events'][0]['message']['text']

            headers = {}
            data = {
                "text": message,
                "chat_id": TG_CHANNEL
            }
            response = requests.get(TG_URL, headers=headers, data=data)
            logging.info('-- Telegram respond')
            logging.info(response.text)
            print('-- Telegram respond')
            print(response.text)

        # Other message type
        if payload['events'][0]['message']['type'] in others_type:
            message = "LINE: (" + fwdmsg + ") sent " + payload['events'][0]['message']['type']

            headers = {}
            data = {
                "text": message,
                "chat_id": TG_CHANNEL
            }

            response = requests.get(TG_URL, headers=headers, data=data)
            logging.info('-- Telegram respond')
            logging.info(response.text)
            print('-- Telegram respond')
            print(response.text)
            
    return '', 200

def get_group_name(source_id):
    headers = { 'Authorization': 'Bearer ' + LINE_TOKEN }
    data = {}

    url = f'https://api.line.me/v2/bot/group/{source_id}/summary'
    r = requests.get(url, headers=headers, data=data).json()

    return r["groupName"]

def get_user_name(source_type, source_id, userid):
    headers = { 'Authorization': 'Bearer ' + LINE_TOKEN }
    data = {}

    url = f'https://api.line.me/v2/bot/{source_type}/{source_id}/member/{userid}'
    r = requests.get(url, headers=headers, data=data).json()

    return r["displayName"]

