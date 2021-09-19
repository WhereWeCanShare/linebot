from flask import Blueprint, request
import os
import datetime
import requests
import logging

# get the key from system variables in .env
LINE_TOKEN = os.getenv("LINE_TOKEN")
TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHANNEL = os.getenv("TG_CHANNEL")
TG_URL = f'https://api.telegram.org/bot{TG_TOKEN}/sendmessage'

## initial all variable
discard_events = ['join', 'leave', 'memberJoined', 'memberLeft', 'follow', 'unfollow', 'leave', 'postback', 'beacon', 'accountLink', 'things', ]
others_type = ['image', 'image', 'sticker']

logging.basicConfig(filename='line2telegram.log',
                    level=logging.DEBUG, format='')

l2tg = Blueprint('l2tg', __name__)

@l2tg.route('/', methods=['POST', 'GET'])
def l2tg_main():
    
    if request.method == 'POST':
        payload = request.json
    
        # logging to file.
        logging.info(f'\n--- Webhook {datetime.datetime.today()}')
        logging.info(payload)

        # discard some LINE events.
        if payload['events'][0]['type'] in discard_events:
            return '.l.', 200

        fwdmsg = ''

        #
        logging.info(f'LINE_TOKEN = {LINE_TOKEN}')
        logging.info(f'TG_TOKEN = {TG_TOKEN}')
        logging.info(f'TG_CHANNEL = {TG_CHANNEL}')
        #

        headers = { 'Authorization': 'Bearer ' + LINE_TOKEN }
        data = {}

        # GROUP info
        if payload['events'][0]['source']['type'] == 'group':
            groupid = payload['events'][0]['source']['groupId']
            userid = payload['events'][0]['source']['userId']

            fwdmsg = get_user_name(groupid, userid) + " in " + get_group_name(groupid)

        # ROOM info
        if payload['events'][0]['source']['type'] == 'room':
            roomid = payload['events'][0]['source']['roomId']
            userid = payload['events'][0]['source']['userId']

            fwdmsg = get_user_name(roomid, userid) + " in room."

        # check only text type will forward to Telegram
        if payload['events'][0]['message']['type'] == 'text':
            message = "LINE: " + fwdmsg + "\n\n"
            message += payload['events'][0]['message']['text']

            headers = {}
            data = {
                "text": message,
                "chat_id": TG_CHANNEL
            }
            response = requests.get(TG_URL, headers=headers, data=data)
            logging.info(response.text)

        # Other message type
        if payload['events'][0]['message']['type'] in others_type:
            message = "LINE:" + fwdmsg + " sent " + payload['events'][0]['message']['type']

            headers = {}
            data = {
                "text": message,
                "chat_id": TG_CHANNEL
            }

            response = requests.get(TG_URL, headers=headers, data=data)
            logging.info(response.text)
            
    return '', 200

def get_group_name(source_type):
    # headers = { 'Authorization': 'Bearer ' + LINE_TOKEN }
    # data = {}

    url = f'https://api.line.me/v2/bot/group/{source_type}/summary'
    r = requests.get(url, headers=headers, data=data).json()
    grpname = r["groupName"]

    return grpname

def get_user_name(source_type, userid):
    # headers = { 'Authorization': 'Bearer ' + LINE_TOKEN }
    # data = {}

    url = f'https://api.line.me/v2/bot/room/{source_type}/member/{userid}'
    r = requests.get(url, headers=headers, data=data).json()
    usrname = r["displayName"]

    return usrname

