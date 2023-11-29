from telethon import TelegramClient, events
from deep_translator import GoogleTranslator
import os 

DEV = False
if DEV:
    from dotenv import load_dotenv
    load_dotenv()
    APP_ID=os.getenv('APP_ID')
    API_HASH=os.getenv('API_HASH')
else:
    try:
        APP_ID=os.environ.get('APP_ID')
        API_HASH=os.environ.get('API_HASH')
    except Exception as e:
        print(e)
        pass

monitored_channel_id = ['gazaalannet','companion_dev', 'pythontelegrambotgroup', 'TelegramTips']

tarfet_channel_id = 'globchaniniw'

client = TelegramClient('anon', APP_ID, API_HASH)

@client.on(events.NewMessage(chats=monitored_channel_id))
async def new_message_listener(event):
    # print(event)
    try: 
        translated_text = GoogleTranslator(source='auto', target='iw').translate(event.message.message)
        event.message.message = translated_text
        # print channel name 
        await client.send_message(tarfet_channel_id, f"From: {event.chat.title}")
        await client.send_message(tarfet_channel_id, event.message)
    except Exception as e:
        print(e)
        pass
    

client.start()
client.run_until_disconnected()