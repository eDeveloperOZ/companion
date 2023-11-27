import logging
from deep_translator import GoogleTranslator

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import(
    ApplicationBuilder,
      CommandHandler,
      ConversationHandler,
      MessageHandler,
      CallbackQueryHandler,
      filters
)

from ..utils.handlers import *
from ..utils.constants import *
# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
 
# handlers = {
#     'start': CommandHandler(['start','help'], start),
# }

async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
            InlineKeyboardButton("Done", callback_data=str(DONE)),
        ]
    reply_markup = InlineKeyboardMarkup([keyboard])
    await query.edit_message_text('Input a message to translate or press Done for main menu', reply_markup=reply_markup)
    return TRANSLATE

async def proccess_user_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        translated_text = GoogleTranslator(source='auto', target='iw').translate(user_input)
    except Exception as e:
        logger.error(e)
        await update.message.reply_text(f"Error: {e}")
        return TRANSLATE
    await update.message.reply_text(f"Translation:\n {translated_text}")

    keyboard = [
            InlineKeyboardButton("Done", callback_data=str(DONE)),
        ]
    reply_markup = InlineKeyboardMarkup([keyboard])
    await update.message.reply_text('Input a message to translate or press Done for main menu', reply_markup=reply_markup)
    return TRANSLATE

async def input_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle input errors"""
    logger.warning(f"User {update.message.from_user['username']} input error")
    await update.message.reply_text("Please input only text or press Done for main menu")

    keyboard = [
            InlineKeyboardButton("Done", callback_data=str(DONE)),
        ]
    reply_markup = InlineKeyboardMarkup([keyboard])
    await update.message.reply_text('Input a message to translate or press Done for main menu', reply_markup=reply_markup)
    return TRANSLATE

async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # logging.info(f"Received callback data: {query.data}")

    keyboard = [
            InlineKeyboardButton("Translate text", callback_data=str(TRANSLATE)),
            InlineKeyboardButton("Done", callback_data=str(END_CONVERSATION)),
        ]
    reply_markup = InlineKeyboardMarkup([keyboard])

    await query.edit_message_text('Start menu', reply_markup=reply_markup)
    return CHOOSING

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    '''
    Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    '''
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="See you next time!")
    return ConversationHandler.END

def run_bot():
    application = ApplicationBuilder().token(ACCESS_TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                CallbackQueryHandler(translate_text, pattern='^' + str(TRANSLATE) + '$'),
                CallbackQueryHandler(done, pattern='^' + str(END_CONVERSATION) + '$'),
                CallbackQueryHandler(start_over, pattern='^' + str(DONE) + '$'),
            ],
            TRANSLATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, proccess_user_text),
                MessageHandler(~filters.TEXT & ~filters.COMMAND, input_error),
                CallbackQueryHandler(start_over, pattern='^' + str(DONE) + '$')
            ],
            END_CONVERSATION:[
                CallbackQueryHandler(done, pattern='^' + str(DONE) + '$')
            ]
        },
        fallbacks=[CallbackQueryHandler(done, pattern='^' + str(DONE) + '$')]
    )

    # Add ConversationHandler to application
    application.add_handler(conversation_handler)

    # Run the bot
    application.run_polling()
