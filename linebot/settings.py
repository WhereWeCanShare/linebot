import os
from dotenv import load_dotenv
load_dotenv()

class Setting(object):
    LINE_TOKEN = os.getenv("LINE_TOKEN")
    TG_TOKEN = os.getenv("TG_TOKEN")
    TG_CHANNEL = os.getenv("TG_CHANNEL")
    SKIP_USER_ID = os.getenv("SKIP_USER_ID")

    LOGFILE = os.getenv("LOGFILE") or "../logs/bot.log"
