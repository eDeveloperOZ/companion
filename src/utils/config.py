from dotenv import load_dotenv
import os

class Config:
    DEV = False
    MONITORED_CHANNEL_IDS = [
        'gazaalannet', 'companion_dev', 'Hezbollah', 'gazaalanpa',
        'Electrohizbullah', 'farsna', 'parsine', 'Tasnimnews',
        'gazatv2', 'AjaNews', 'almanarnews', 'GazaNewsNow',
        'ahfadalbahaa', 'sepah_pasdaran', 'NewsPs0', 'MohamadDabaa',
        'hamaas_ps', 'kataebabuali2', 'abuhamzasarayaa', 'alidaralipress',
        'TahrirPulse1', 'Eye_of_resistance', 'From_hebron', 'telepressnews',
        'FarsNewsInt',
    ]

    @classmethod
    def load_environment(cls):
        load_dotenv()
        cls.APP_ID = os.getenv('APP_ID', 'default_app_id')
        cls.API_HASH = os.getenv('API_HASH', 'default_api_hash')
        cls.ACCESS_TOKEN = os.getenv('API_TOKEN', 'default_token')

    @classmethod
    def get_monitored_channels(cls):
        return cls.MONITORED_CHANNEL_IDS

# Load the environment variables when the module is imported
Config.load_environment()
