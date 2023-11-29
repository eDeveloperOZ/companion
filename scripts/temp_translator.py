from telethon import TelegramClient, events
from deep_translator import GoogleTranslator
import os 

DEV = True
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

monitored_channel_id = ['gazaalannet','companion_dev', 'gazaalannetgroup', 'gazaalanpa', 'farsna']
tarfet_channel_id = 'globchaniniw'
client = TelegramClient('anon', APP_ID, API_HASH)

processed_group_ids = set()

@client.on(events.NewMessage(chats=monitored_channel_id))
async def new_message_listener(event):
    print(f"Received message ID: {event.message.id} with Group ID: {event.message.grouped_id}")

    # Determine if this is a new group or a single message
    is_new_group_or_message = False
    group_id = event.message.grouped_id

    # If it's a single message, use its ID as the group identifier
    if group_id is None:
        group_id = event.message.id
        is_new_group_or_message = True  # Since it's a single message, it's always "new"

    # If we have not processed this group_id before, mark it as new
    if group_id not in processed_group_ids:
        is_new_group_or_message = True
        processed_group_ids.add(group_id)

    # If it's a new group or message, send the "From" line
    if is_new_group_or_message:
        await client.send_message(tarfet_channel_id, f"From: {event.chat.title}")

    # Now process and send the message content
    try:
        # Translate the message
        translated_text = GoogleTranslator(source='auto', target='iw').translate(event.message.message)
        event.message.message = translated_text
        # Send the translated message content
        await client.send_message(tarfet_channel_id, event.message)
    except Exception as e:
        print(e)
    

client.start()
client.run_until_disconnected()