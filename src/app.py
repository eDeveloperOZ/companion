from telethon import TelegramClient, events
from .translator import ChannelTranslator
from .duplicate_scanner import DuplicateScanner
from .content_manager import ContentManager
from .utils.config import Config
from .utils.constants import TARGET_CHANNEL_ID, MODEL_PATH
import asyncio

class App:
    def __init__(self):
        self.client = TelegramClient('anon', Config.APP_ID, Config.API_HASH)
        self.translator = ChannelTranslator()
        self.scanner = DuplicateScanner()
        self.content_manager = ContentManager(MODEL_PATH)
        self.monitored_channel_id = Config.get_monitored_channels()
        self.processed_group_ids = set()
        self.client.add_event_handler(self.new_message_listener, events.NewMessage(chats=self.monitored_channel_id))

    async def new_message_listener(self, event):
        try:
            if Config.DEV:
                print(f"Received message ID: {event.message.id} with Group ID: {event.message.grouped_id}")

            group_id = event.message.grouped_id or event.message.id
            # Check if a channel has sent a lot of messages at once
            if group_id not in self.processed_group_ids:
                self.processed_group_ids.add(group_id)
                last_messages = await self.client.get_messages(TARGET_CHANNEL_ID, limit=25)

                # Perform translation regardless of message type TODO: translate other types
                translated_text = await self.translator.translate_message(event.message.message)
                similarity = await self.translator.is_message_similar(event.message.message, last_messages)

                # Process only if the message is text-based and not similar to previous messages
                if event.message.media is None and not similarity:
                    # Proccess the text to make a decision if it is interesting based on our traind model
                    decision_to_post = await self.content_manager.decide(translated_text)
                    if decision_to_post:
                        print(f"Text message {event.message.id} is not similar to previous messages or spam, sending...")
                        event.message.message = translated_text
                        await self.client.send_message(TARGET_CHANNEL_ID, event.message)
                    else:
                        print(f"Text message {event.message.id} was tagged as spam or non-interesting, skipping...")
                else:
                    # For non-text messages or similar text messages TODO: handle video/image/audio
                    print(f"Non-text or similar text message {event.message.id}, sending...")
                    event.message.message = translated_text
                    await self.client.send_message(TARGET_CHANNEL_ID, event.message)

        except Exception as e:
            print(f"Error in new_message_listener: {e}")

    async def run(self):
        await self.client.start()
        scanner_task = asyncio.create_task(self.scanner.run())
        await self.client.run_until_disconnected()
        await scanner_task
