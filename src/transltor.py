





class Transltor():
    def __init__(self): 
        self.client = TelegramClient('anon', api_id, api_hash)
        self.processed_group_ids = set()
        