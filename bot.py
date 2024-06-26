import logging
from re import search
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CommandHandler, CallbackContext, Application, MessageHandler, filters, InlineQueryHandler
import os
from dotenv import load_dotenv
from languages import sendTranslatedMessage
from linkEmbedding import inlineFurAffinity, inlineInsta, inlineTiktok, inlineTrackerRemoval, inlineTwitter, twitter, tiktok, insta, furAffinity, trackerRemoval, trackerRegexPattern

if 'TOKEN' not in os.environ:
    load_dotenv()

TOKEN = os.getenv('TOKEN')
WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = os.getenv('PORT')
KEY_PATH = os.getenv('KEY_PATH', None)
CERT_PATH = os.getenv('CERT_PATH', None)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    await sendTranslatedMessage(update,'motd')

async def inlineMessage(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    if not query:
        return
    if search(r'(twitter|x)\.com/.+/status/[0-9]+',query):
        await inlineTwitter(update)
    elif search(r'tiktok\.com/.+',query):
        await inlineTiktok(update)
    elif search(r'instagram\.com/reel/.+', query):
        await inlineInsta(update)
    elif search(r'furaffinity\.net/view/.+', query):
        await inlineFurAffinity(update)
    elif search(trackerRegexPattern, query):
        await inlineTrackerRemoval(update)
    else:
        return
        
async def privateMessage(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    if not message:
        return
    if search(r'(twitter|x)\.com/.+/status/[0-9]+', message):
        await twitter(update)
    elif search(r'tiktok\.com/.+', message):
        await tiktok(update)
    elif search(r'instagram\.com/reel/.+', message):
        await insta(update)
    elif search(r'furaffinity\.net/view/.+', message):
        await furAffinity(update)
    elif search(trackerRegexPattern, message):
        await trackerRemoval(update)
    else:
        await sendTranslatedMessage(update,'unknownMessage')

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, privateMessage))
    application.add_handler(InlineQueryHandler(inlineMessage))
    if not KEY_PATH:
        application.run_webhook(listen='0.0.0.0', port=PORT, secret_token=WEBHOOK_TOKEN, webhook_url=WEBHOOK_URL+PORT)
    else:
        application.run_webhook(listen='0.0.0.0', port=PORT, secret_token=WEBHOOK_TOKEN, key=KEY_PATH, cert=CERT_PATH, webhook_url=WEBHOOK_URL+PORT)
    
if __name__ == '__main__':
    main()
