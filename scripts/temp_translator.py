from telethon import TelegramClient, events
from deep_translator import GoogleTranslator
import asyncio
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
buffered_messages = {}
buffer_timers = {}

client = TelegramClient('anon', APP_ID, API_HASH)

async def send_buffered_messages(channel_id):
    if channel_id in buffered_messages:
        messages = buffered_messages.pop(channel_id)
        text_to_send = f"From: {messages[0].chat.title}\n" + "\n".join(
            [GoogleTranslator(source='auto', target='iw').translate(message.message.message) for message in messages]
        )
        await client.send_message(tarfet_channel_id, text_to_send)
        # Clear the timer for this channel_id
        buffer_timers.pop(channel_id, None)


@client.on(events.NewMessage(chats=monitored_channel_id))
async def new_message_listener(event):
    channel_id = event.chat_id
    
    # If this is the first message from this channel or a timer isn't already set, send the title
    if channel_id not in buffered_messages:
        await client.send_message(tarfet_channel_id, f"From: {event.chat.title}")
    
    # Add the message to the buffer
    if channel_id not in buffered_messages:
        buffered_messages[channel_id] = [event]
    else:
        buffered_messages[channel_id].append(event)
    
    # If a timer is running, cancel it and start a new one
    if channel_id in buffer_timers:
        buffer_timers[channel_id].cancel()
    
    # Set a timer to send messages after a delay (2 seconds)
    buffer_timers[channel_id] = asyncio.get_event_loop().call_later(2, lambda: asyncio.create_task(send_buffered_messages(channel_id)))
    

client.start()
client.run_until_disconnected()