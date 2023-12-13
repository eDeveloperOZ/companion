import asyncio
from telethon import TelegramClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from datetime import datetime

# Load environment variables
DEV = False  # Set this to False in production
if DEV:
    from dotenv import load_dotenv
    load_dotenv()
    APP_ID = os.getenv('APP_ID')
    API_HASH = os.getenv('API_HASH')
else:
    APP_ID = os.environ.get('APP_ID')
    API_HASH = os.environ.get('API_HASH')

CHANNEL_TO_SCAN = 'globchaniniw'

class TextMessage:
    def __init__(self, id, timestamp, content):
        self.id = id
        self.timestamp = timestamp
        self.content = content

    def __repr__(self):
        return f"{self.id}, {self.timestamp}, {self.content}"

# Function to fetch all messages from a channel
async def fetch_all_messages(client, channel):
    print("Fetching all messages...")
    all_messages = []
    last_message_id = None
    async for message in client.iter_messages(channel):
        if not last_message_id:
            last_message_id = message.id  # Capture the first (latest) message ID
        if message.text and 'From:' not in message.text:
            all_messages.append(TextMessage(message.id, message.date, message.text))
    print(f"Found {len(all_messages)} messages")
    return all_messages, last_message_id

# Function to find similar messages and simulate deletion
async def find_and_delete_similar_messages(client, messages, similarity_threshold=0.7):
    print("Finding similar messages...")
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([msg.content for msg in messages])
    cosine_sim = cosine_similarity(tfidf_matrix)

    processed = [False] * len(messages)
    total_messages_to_delete = 0

    for i in range(len(messages)):
        if not processed[i]:
            similar_batch = [(messages[i], i)]
            processed[i] = True

            for j in range(i+1, len(messages)):
                if cosine_sim[i, j] > similarity_threshold and not processed[j]:
                    similar_batch.append((messages[j], j))
                    processed[j] = True

            if len(similar_batch) > 1:
                # Sort similar messages by timestamp, keeping the oldest message
                similar_batch.sort(key=lambda x: x[0].timestamp)
                messages_to_delete = [msg[0].id for msg in similar_batch[1:]]


                for msg_id in messages_to_delete:
                    await client.delete_messages(CHANNEL_TO_SCAN, [msg_id])
                    total_messages_to_delete += 1

    return total_messages_to_delete


# Function to wait until the next round hour
async def wait_for_twenty_minutes():
    while True:
        now = datetime.now()
        if now.minute % 20 == 0 and now.second == 0:
            break
        await asyncio.sleep(1)  # Wait 1 second before checking again

# Main execution function
async def main():
    client = TelegramClient('scanner', APP_ID, API_HASH)
    await client.start()

    while True:  # Continuous loop
        if not DEV:
            await wait_for_twenty_minutes()  # Wait until the next round hour
        
        all_messages, last_message_id = await fetch_all_messages(client, CHANNEL_TO_SCAN)

        # Process in batches of 1000
        batch_size = 1000
        total_deleted = 0
        for start_index in range(0, len(all_messages), batch_size):
            end_index = min(start_index + batch_size, len(all_messages))
            batch = all_messages[start_index:end_index]
            print(f"Processing messages {start_index} to {end_index - 1}")
            total_deleted += await find_and_delete_similar_messages(client, batch)

        report_message = f"🚨🚨🚨 **Important Channel Update** 🚨🚨🚨\n\n**{total_deleted} duplicate messages were removed!**\n\n"
        await client.send_message(CHANNEL_TO_SCAN, report_message, parse_mode='md')

        print(f"Process started from message ID: {last_message_id}")

# Run the script
if __name__ == '__main__':
    asyncio.run(main())
