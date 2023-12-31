from pathlib import Path
from .config import Config


TARGET_CHANNEL_ID = 'globchaniniw'

# Paths
PROJECT_DIR = Path(__file__).parent.parent.parent

DATA_DIR = PROJECT_DIR / 'data'
SRC_DIR = PROJECT_DIR / 'src'
UTILS_DIR = SRC_DIR / 'utils'
LOGS_DIR = PROJECT_DIR / 'logs'
DOCS_DIR = PROJECT_DIR / 'docs'

if Config.DEV:
    MODEL_PATH = DATA_DIR / 'model'
else:
    MODEL_PATH = Path('/opt/model') 

