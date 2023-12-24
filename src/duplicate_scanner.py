import asyncio
from telethon import TelegramClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from datetime import datetime
from .utils.config import Config

class DuplicateScanner:
    def __init__(self):
        self.client = TelegramClient('scanner', Config.APP_ID, Config.API_HASH)
        self.channel_to_scan = 'globchaniniw'

    class TextMessage:
        def __init__(self, id, timestamp, content):
            self.id = id
            self.timestamp = timestamp
            self.content = content

        def __repr__(self):
            return f"{self.id}, {self.timestamp}, {self.content}"

    async def fetch_all_messages(self):
        print("Fetching all messages...")
        all_messages = []
        async for message in self.client.iter_messages(self.channel_to_scan):
            if message.text and 'From:' not in message.text:
                all_messages.append(self.TextMessage(message.id, message.date, message.text))
        print(f"Found {len(all_messages)} messages")
        return all_messages

    async def find_and_delete_similar_messages(self, messages, similarity_threshold=0.7):
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
                    similar_batch.sort(key=lambda x: x[0].timestamp)  # Keeping the oldest message
                    messages_to_delete = [msg[0].id for msg in similar_batch[1:]]

                    for msg_id in messages_to_delete:
                        await self.client.delete_messages(self.channel_to_scan, [msg_id])
                        total_messages_to_delete += 1

        return total_messages_to_delete

    async def wait_for_twenty_minutes(self):
        while True:
            now = datetime.now()
            if now.minute % 20 == 0 and now.second == 0:
                break
            await asyncio.sleep(1)  # Wait 1 second before checking again

    async def run(self):
        await self.client.start()
        while True:  # Continuous loop
            if not Config.DEV:
                await self.wait_for_twenty_minutes()
            
            all_messages = await self.fetch_all_messages()

            # Process in batches of 1000
            batch_size = 1000
            total_deleted = 0
            for start_index in range(0, len(all_messages), batch_size):
                end_index = min(start_index + batch_size, len(all_messages))
                batch = all_messages[start_index:end_index]
                print(f"Processing messages {start_index} to {end_index - 1}")
                total_deleted += await self.find_and_delete_similar_messages(batch)

            report_message = f"🚨🚨🚨 **Important Channel Update** 🚨🚨🚨\n\n**{total_deleted} duplicate messages were removed!**\n\n"
            await self.client.send_message(self.channel_to_scan, report_message, parse_mode='md')
            print("Scan complete for this cycle.")

