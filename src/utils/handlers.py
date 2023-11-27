from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ContextTypes

from ..utils.constants import END_CONVERSATION, TRANSLATE, CHOOSING

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a message when the command /start is issued."""
    user = update.message.from_user
    # logger.info("User %s started the conversation.", user.first_name)
    keyboard = [
            InlineKeyboardButton("Translate text", callback_data=str(TRANSLATE)),
            InlineKeyboardButton("Done", callback_data=str(END_CONVERSATION)),
    ]
    reply_markup = InlineKeyboardMarkup([keyboard])
    await update.message.reply_text('Welcome to the Companion bot!', reply_markup=reply_markup)
    
    return CHOOSING