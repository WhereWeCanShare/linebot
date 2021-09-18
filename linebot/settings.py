import os
from dotenv import load_dotenv
load_dotenv()

# read the system variable to application variable.
# update these according to your application.
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False

BTS_CHANNEL_SECRET = os.environ.get('BTS_CHANNEL_SECRET')
BTS_CHANNEL_ACCESS_TOKEN = os.environ.get('BTS_CHANNEL_ACCESS_TOKEN')
