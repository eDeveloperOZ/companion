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

monitored_channel_id = ['gazaalannet','companion_dev', 'gazaalannetgroup', 'gazaalanpa']
tarfet_channel_id = 'globchaniniw'
echoed_channels = {}

client = TelegramClient('anon', APP_ID, API_HASH)

@client.on(events.NewMessage(chats=monitored_channel_id))
async def new_message_listener(event):
    # print(event)
    try:
        channel_id = event.chat_id
        # Check if we have already echoed for this channel
        if channel_id not in echoed_channels:
            # Send the channel title once
            await client.send_message(tarfet_channel_id, f"From: {event.chat.title}")
            # Mark this channel as echoed
            echoed_channels[channel_id] = True
        
        # Translate and send the message
        translated_text = GoogleTranslator(source='auto', target='iw').translate(event.message.message)
        await client.send_message(tarfet_channel_id, translated_text)
    except Exception as e:
        print(e)
    

client.start()
client.run_until_disconnected()