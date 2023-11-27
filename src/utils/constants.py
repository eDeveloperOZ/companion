from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get API token from .env file
ACCESS_TOKEN = os.getenv('API_TOKEN')

# States
# = range(2)

# callback_data
TRANSLATE, DONE, START_OVER, CHOOSING, END_CONVERSATION = range(5)