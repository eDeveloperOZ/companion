# app.py
from telethon import TelegramClient, events
from translator import ChannelTranslator
from duplicate_scanner import DuplicateScanner
from .utils.config import Config
from .utils.constants import TARGET_CHANNEL_ID
import asyncio

class App:
    def __init__(self):
        self.client = TelegramClient('anon', Config.APP_ID, Config.API_HASH)
        self.translator = ChannelTranslator()
        self.scanner = DuplicateScanner()
        self.monitored_channel_id = Config.get_monitored_channels()
        self.processed_group_ids = set()
        self.client.add_event_handler(self.new_message_listener, events.NewMessage(chats=self.monitored_channel_id))


    async def new_message_listener(self, event):
        print(f"Received message ID: {event.message.id} with Group ID: {event.message.grouped_id}")

        group_id = event.message.grouped_id
        if group_id is None:
            group_id = event.message.id
            is_new_group_or_message = True
        else:
            is_new_group_or_message = group_id not in self.processed_group_ids

        if is_new_group_or_message:
            self.processed_group_ids.add(group_id)
            last_messages = await self.client.get_messages(TARGET_CHANNEL_ID, limit=25)
            if not await self.translator.is_message_similar(event.message.message, last_messages):
                translated_text = await self.translator.translate_message(event.message.message)
                if translated_text:
                    event.message.message = translated_text
                    await self.client.send_message(TARGET_CHANNEL_ID, event.message)

    async def run(self):
        await self.client.start()
        scanner_task = asyncio.create_task(self.scanner.run())
        await self.client.run_until_disconnected()
        await scanner_task

