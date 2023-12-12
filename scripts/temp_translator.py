from telethon import TelegramClient, events
from deep_translator import GoogleTranslator
import os 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import asyncio


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

monitored_channel_id = [
    'gazaalannet', 'companion_dev', 'Hezbollah', 'gazaalanpa',
    'Electrohizbullah','farsna', 'parsine', 'Tasnimnews',
    'gazatv2', 'AjaNews', 'almanarnews','GazaNewsNow', 
    'ahfadalbahaa', 'sepah_pasdaran', 'NewsPs0', 'MohamadDabaa',
    'hamaas_ps', 'kataebabuali2', 'abuhamzasarayaa', 'alidaralipress',
    'TahrirPulse1', 'Eye_of_resistance','From_hebron', 'telepressnews', 
    ]
target_channel_id = 'globchaniniw'
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

    # If the message is not similar to any of the last 10 messages, send it
    if not await is_message_similar(client, event.message.message):
        print(f"Message {event.message.id} is not similar to previous messages, sending...")
        # If it's a new group or message, send the "From" line
        if is_new_group_or_message:
            # translate chat title to hebrew
            try:
                translated_title = GoogleTranslator(source='auto', target='iw').translate(event.chat.title)
                await client.send_message(target_channel_id, f"From: {event.chat.title}({translated_title})")
            except Exception as e:
                print(e)
                await client.send_message(target_channel_id, f"From: {event.chat.title}")

        # Now process and send the message content
        try:
            # Translate the message
            translated_text = GoogleTranslator(source='auto', target='iw').translate(event.message.message)
            event.message.message = translated_text
            # Send the translated message content
            await client.send_message(target_channel_id, event.message)
        except Exception as e:
            print(e)
    else:
        print(f"Message {event.message.id} is similar to previous messages, skipping...")
    

async def is_message_similar(client, new_message, similarity_threshold=0.7):
    # wait for 0.1 seconds
    await asyncio.sleep(0.1)
    # Fetch last 10 messages from the target channel
    last_messages = await client.get_messages(target_channel_id, limit=10)

    # Prepare texts for comparison
    # Translate the new message
    translated_text = GoogleTranslator(source='auto', target='iw').translate(new_message)
    texts = [msg.message for msg in last_messages] + [translated_text]
    if len(texts) < 2:  # Not enough messages to compare
        return False

    # Calculate TF-IDF and cosine similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

    # Check if any message is similar
    return any(similarity >= similarity_threshold for similarity in cosine_sim)


client.start()
client.run_until_disconnected()