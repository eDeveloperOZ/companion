from dotenv import load_dotenv
import os 

class Config():
    DEV = False

    def load_enviroment(self):
        if DEV:
            load_dotenv()
        Config.ACCESS_TOKEN = os.getenv('API_TOKEN', 'default_token')
        Config.APP_ID = os.getenv('APP_ID', 'default_app_id')
        Config.API_HASH = os.getenv('APP_HASH', 'default_api_hash')

    def get_monitored_channels(self):
        return MONITORED_CHANNEL_IDS = [
    'gazaalannet', 'companion_dev', 'Hezbollah', 'gazaalanpa',
    'Electrohizbullah','farsna', 'parsine', 'Tasnimnews',
    'gazatv2', 'AjaNews', 'almanarnews','GazaNewsNow', 
    'ahfadalbahaa', 'sepah_pasdaran', 'NewsPs0', 'MohamadDabaa',
    'hamaas_ps', 'kataebabuali2', 'abuhamzasarayaa', 'alidaralipress',
    'TahrirPulse1', 'Eye_of_resistance','From_hebron', 'telepressnews',
    'FarsNewsInt', 
    ]
# Load the enviroment variables when the module is imported
Config().load_enviroment()