from dotenv import load_dotenv
import os

# Load .env file
DEV = False
if DEV:
    load_dotenv()
    # Get API token from .env file
    ACCESS_TOKEN = os.getenv('API_TOKEN')
else:
    # Get API token from Heroku config vars
    ACCESS_TOKEN = os.environ.get('API_TOKEN')
    print(f'got token {ACCESS_TOKEN}')

# States
# = range(2)

# callback_data
TRANSLATE, DONE, START_OVER, CHOOSING, END_CONVERSATION = range(5)