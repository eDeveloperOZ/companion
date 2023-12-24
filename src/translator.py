# translator.py
from deep_translator import GoogleTranslator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ChannelTranslator:
    @staticmethod
    async def is_message_similar(new_message, last_messages, similarity_threshold=0.7):
        if new_message is None:
            return False

        try:
            translated_text = GoogleTranslator(source='auto', target='iw').translate(new_message)
            if translated_text is None or translated_text.strip() == '':
                return False
        except Exception as e:
            print(f"Translation failed: {e}")
            return False

        texts = [msg.message for msg in last_messages if msg.message and msg.message.strip() != '']
        if len(texts) == 0:
            return False

        texts.append(translated_text)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(texts)
        cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

        return any(similarity >= similarity_threshold for similarity in cosine_sim)

    @staticmethod
    async def translate_message(message):
        try:
            return GoogleTranslator(source='auto', target='iw').translate(message)
        except Exception as e:
            print(e)
            return None
