from flask import Blueprint, request
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
TG_URL_PHOTO = f'https://api.telegram.org/bot{TG_TOKEN}/sendphoto]'

LOGFILE = os.getenv('LOGFILE')

## initial all variable
discard_events = ['join', 'leave', 'memberJoined', 'memberLeft', 'follow', 'unfollow', 'leave', 'postback', 'beacon', 'accountLink', 'things', ]
others_type = ['video', 'sticker', 'file']

logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, format='')
logging.info(f'\n=== Service start {datetime.datetime.today()}')
print(f'\n=== Service start {datetime.datetime.today()}')


l2tg = Blueprint('l2tg', __name__)

@l2tg.route('/', methods=['POST', 'GET'])
def l2tg_main():
    
    if request.method == 'POST':
        payload = request.json
    
        # logging to file.
        msginfo = f'\n--- Webhook {datetime.datetime.today()}'
        logging.info(msginfo)
        logging.info(payload)
        print(msginfo)
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
            msginfo = '-- Telegram respond'
            logging.info(msginfo)
            logging.info(response.text)
            print(msginfo)
            print(response.text)

        # image
        if payload['events'][0]['message']['type'] == 'image':
            message = "LINE: (" + fwdmsg + ") sent " + payload['events'][0]['message']['type']

            msgid = payload['events'][0]['message']['id']
            flenm = '{}.jpg'.format(payload['events'][0]['timestamp'])

            url = f'https://api-data.line.me/v2/bot/message/{msgid}/content'

            Authorization = 'Bearer {}'.format(LINE_TOKEN)
            headers = {
                'Authorization': Authorization
            }

            with open(flenm, 'bw') as f:
                img = requests.get(url, headers=headers)
                f.write(img.content)

            headers = {}
            with open(flenm, 'rb') as f:
                photo = f.read()
                data = {
                    "photo": photo,
                    "chat_id": TG_CHANNEL,
                    "caption": fwdmsg
                }
                response = requests.get(TG_URL_PHOTO, headers=headers, data=data)
            
            msginfo = '-- Telegram respond'
            logging.info(msginfo)
            logging.info(response.text)
            print(msginfo)
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
            msginfo = '-- Telegram respond'
            logging.info(msginfo)
            logging.info(response.text)
            print(msginfo)
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

