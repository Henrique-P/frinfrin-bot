import logging, requests
from re import search
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CommandHandler, CallbackContext, Application, MessageHandler, filters, CallbackQueryHandler, InlineQueryHandler
import os
# from game import rps, rpsStart
from dotenv import load_dotenv
from linkEmbedding import twitter, tiktok, insta, trackerRemoval

if 'TOKEN' not in os.environ:
    load_dotenv()

TOKEN = os.getenv('TOKEN')
WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = os.getenv('PORT')
KEY_PATH = os.getenv('KEY_PATH', None)
CERT_PATH = os.getenv('CERT_PATH', None)

trackerRegexPattern = r'&?si=[^&]*|&?igsh=[^&]*'

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    user =  update.effective_user.full_name
    logging.info("%s started the bot", user)
    await update.message.reply_text("Hello! Send me a Twitter, TikTok or Instagram link.")
        
async def inlineMessage(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    user = update.inline_query.from_user
    if not query:
        return
    if search(r'(twitter|x)\.com/.+/status/.+',query):
        response = twitter(query)
        logging.info("FxTwitter Request by %s", user)
    elif search(r'tiktok\.com/@.+/video/.+',query):
        response = tiktok(query)
        logging.info("FxTikTok Request by %s", user)
    elif search(r'instagram\.com/reel/.+', query):
        response = insta(query)
        logging.info("DDInstagram Request by %s", user)
    elif search(trackerRegexPattern, query):
        response = trackerRemoval(query)
        logging.info("Generic Tracker Removal Request by %s", user)
    else:
        return
    if query == response:
        return
    elif not response:
        return
    answer = [InlineQueryResultArticle(response,'Interactive',InputTextMessageContent(response),description='Send an Interactive View link')]
    await update.inline_query.answer(answer)
        
async def privateMessage(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    user = update.effective_user.full_name
    if not message:
        return
    if search(r'(twitter|x)\.com/.+/status/.+', message):
        response = twitter(message)
        logging.info("FxTwitter Request by %s", user)
    elif search(r'tiktok\.com/@.+/video/.+', message):
        response = tiktok(message)
        logging.info("FxTikTok Request by %s", user)
    elif search(r'instagram\.com/reel/.+', message):
        response = insta(message)
        logging.info("DDInstagram Request by %s", user)
    elif search(trackerRegexPattern, message):
        response = trackerRemoval(message)
        logging.info("Generic Tracker Removal Request by %s", user)
    else:
        return
    if message == response:
        logging.info("¯\\_(ツ)_/¯")
        await update.message.reply_sticker("CAACAgEAAxkBAAECSm9mXAHqyk3h8vkRx7ucxyF6qQppkAACuQIAAh9lSEfeZwF56Y_N9DUE")
        return
    elif not response:
        logging.info("%s got RickRoll'd", user)
        await update.message.reply_text("Here's your link:\nhttps://youtu.be/dQw4w9WgXcQ", disable_web_page_preview=True)
        return
    await update.message.reply_text("Here's your link:")
    await update.message.reply_text(response)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, privateMessage))
    application.add_handler(InlineQueryHandler(inlineMessage))
    if not KEY_PATH:
        application.run_webhook(listen='0.0.0.0', port=PORT, secret_token=WEBHOOK_TOKEN, webhook_url=WEBHOOK_URL+PORT)
    else:
        application.run_webhook(listen='0.0.0.0', port=PORT, secret_token=WEBHOOK_TOKEN, key=KEY_PATH, cert=CERT_PATH, webhook_url=WEBHOOK_URL+PORT)
    

if __name__ == '__main__':
    main()
