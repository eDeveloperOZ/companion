from dotenv import load_dotenv
import os

# Load .env file
DEV = False
if DEV:
    load_dotenv()
    # Get API token from .env file
    ACCESS_TOKEN = os.getenv('API_TOKEN')
    APP_ID=os.getenv('APP_ID')
    APP_HASH=os.getenv('APP_HASH')
else:
    # Get API token from Heroku config vars
    ACCESS_TOKEN = os.environ.get('API_TOKEN')
    APP_ID=os.environ.get('APP_ID')
    APP_HASH=os.environ.get('APP_HASH')
# States
# = range(2)

# callback_data
TRANSLATE, DONE, START_OVER, CHOOSING, END_CONVERSATION = range(5)