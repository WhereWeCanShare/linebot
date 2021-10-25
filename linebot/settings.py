import os
from dotenv import load_dotenv
load_dotenv()

class Setting(object):
    LINE_TOKEN = os.environ.get('LINE_TOKEN')
    TG_TOKEN = os.environ.get("TG_TOKEN")
    TG_CHANNEL = os.environ.get("TG_CHANNEL")
    SKIP_USER_ID = os.environ.get("SKIP_USER_ID")

    LOGFILE = os.environ.get("LOGFILE") or "../logs/bot.log"
