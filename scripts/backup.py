import asyncio
from telethon import TelegramClient
import os

# Load environment variables
DEV = True  # Set this to False in production
if DEV:
    from dotenv import load_dotenv
    load_dotenv()
    APP_ID = os.getenv('APP_ID')
    API_HASH = os.getenv('API_HASH')
else:
    APP_ID = os.environ.get('APP_ID')
    API_HASH = os.environ.get('API_HASH')

MAIN_CHANNEL = 'globchaniniw'
BACKUP_CHANNEL = 'globchaniniwbackup'

async def backup_channel(client):
    print(f"Starting backup of {MAIN_CHANNEL} to {BACKUP_CHANNEL}...")
    async for message in client.iter_messages(MAIN_CHANNEL):
        await client.forward_messages(BACKUP_CHANNEL, message)
    print("Backup completed successfully.")

async def main():
    client = TelegramClient('backup_session', APP_ID, API_HASH)
    await client.start()

    await backup_channel(client)

if __name__ == '__main__':
    asyncio.run(main())
