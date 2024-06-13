import logging
import time
from re import search
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CommandHandler, CallbackContext, Application, MessageHandler, filters, InlineQueryHandler
import os
from dotenv import load_dotenv
from linkEmbedding import twitter, tiktok, insta, furAffinity, trackerRemoval, trackerRegexPattern

if 'TOKEN' not in os.environ:
    load_dotenv()

TOKEN = os.getenv('TOKEN')
WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = os.getenv('PORT')
KEY_PATH = os.getenv('KEY_PATH', None)
CERT_PATH = os.getenv('CERT_PATH', None)

userRegistry = {"linkX": 0, "linkInsta": 0, "linkFurAffinity": 0, "linkTikTok": 0, "linkGeneric": 0, "genericTxt": 0, "commandStart": 0, "commandLog": 0, "admin": 0, "qa": 0, "noService": 0}
startUpTime= time.ctime()
def printUserRegistry():
    logString = ""
    for key, value in userRegistry.items():        
        logString += f'{key}: {value}\n'
    return logString

def addToRegistry(key: str, user: int, admin= 23742393):
    if user != admin:
        userRegistry[key] += 1
    else:
        userRegistry["admin"] += 1

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    user =  update.effective_user.id
    # logging.info("%s started the bot", user)
    addToRegistry("commandStart", user)
    await update.message.reply_text("Hello! Send me a Twitter, TikTok or Instagram link.")
    
async def log(update: Update, context: CallbackContext) -> None:
    user =  update.effective_user.id
    # logging.info("%s acessed the log", user)
    addToRegistry("commandLog", user)
    response = printUserRegistry()
    await update.message.reply_text(response)
    await update.message.reply_text(f'Counting Since: {startUpTime}')
        
async def inlineMessage(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    user = update.inline_query.from_user.id
    if not query:
        return
    if search(r'(twitter|x)\.com/.+/status/[0-9]+',query):
        response = twitter(query)
        thumbUrl = 'https://cdn.freelogovectors.net/wp-content/uploads/2023/07/twitter-x-logo-freelogovectors.net_.png'
        title = "X"
        # logging.info("FxTwitter Request by %s", user)
        addToRegistry("linkX", user)
    elif search(r'tiktok\.com/.+',query):
        response = tiktok(query)
        thumbUrl = ''
        title = "TikTok"
        addToRegistry("linkTikTok", user)
        # logging.info("FxTikTok Request by %s", user)
    elif search(r'instagram\.com/reel/.+', query):
        response = insta(query)
        thumbUrl = ''
        title = "Instagram"
        addToRegistry("linkInsta", user)
        # logging.info("DDInstagram Request by %s", user)
    elif search(r'furaffinity\.net/view/.+', query):
        response = furAffinity(query)
        thumbUrl = 'https://logos-world.net/wp-content/uploads/2024/02/FurAffinity-Logo-500x281.png'
        title = "FurAffinity"
        addToRegistry("linkFurAffinity", user)
        # logging.info("FxFurAffinity Request by %s", user)
    elif search(trackerRegexPattern, query):
        response = trackerRemoval(query)
        thumbUrl = ''
        title = "Tracker Removed"
        addToRegistry("genericLink", user)
        # logging.info("Generic Tracker Removal Request by %s", user)
    else:
        return
    if not response or response == -1 or response == query:
        return
    answer = [InlineQueryResultArticle(response, title, InputTextMessageContent(response), thumbnail_url=thumbUrl, description='Send embed, trackerless link')]
    await update.inline_query.answer(answer)
        
async def privateMessage(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    user = update.effective_user.id
    if not message:
        return
    if search(r'(twitter|x)\.com/.+/status/[0-9]+', message):
        response = twitter(message)
        addToRegistry("linkX", user)
        # logging.info("FxTwitter Request by %s", user)
    elif search(r'tiktok\.com/.+', message):
        response = tiktok(message)
        addToRegistry("linkTikTok", user)
        # logging.info("FxTikTok Request by %s", user)
    elif search(r'instagram\.com/reel/.+', message):
        response = insta(message)
        addToRegistry("linkInsta", user)
        # logging.info("DDInstagram Request by %s", user)
    elif search(r'furaffinity\.net/view/.+', message):
        response = furAffinity(message)
        addToRegistry("linkFurAffinity", user)
        # logging.info("FxFurAffinity Request by %s", user)
    elif search(trackerRegexPattern, message):
        response = trackerRemoval(message)
        addToRegistry("linkGenericLink", user)
        # logging.info("Generic Tracker Removal Request by %s", user)
    else:
        addToRegistry("genericTxt", user)
        await update.message.reply_text("Message not recognized. Try sending me a Instagram, Twitter, Furaffinity or TikTok link and I will embed and/or remove any trackers.")
        return
    if message == response:
        addToRegistry("noService", user)
        await update.message.reply_text("Nothing to do with this link.")
        await update.message.reply_sticker("CAACAgEAAxkBAAECSm9mXAHqyk3h8vkRx7ucxyF6qQppkAACuQIAAh9lSEfeZwF56Y_N9DUE")
        return
    elif not response:
        addToRegistry("qa", user)
        await update.message.reply_text("Here's your link:\nhttps://youtu.be/dQw4w9WgXcQ", disable_web_page_preview=True)
        return
    elif response == -1:
        await update.message.reply_text("This URL is either invalid or the content is private.")
        return
    
    await update.message.reply_text("Here's your link:")
    await update.message.reply_text(response)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("log", log))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, privateMessage))
    application.add_handler(InlineQueryHandler(inlineMessage))
    if not KEY_PATH:
        application.run_webhook(listen='0.0.0.0', port=PORT, secret_token=WEBHOOK_TOKEN, webhook_url=WEBHOOK_URL+PORT)
    else:
        application.run_webhook(listen='0.0.0.0', port=PORT, secret_token=WEBHOOK_TOKEN, key=KEY_PATH, cert=CERT_PATH, webhook_url=WEBHOOK_URL+PORT)
    

if __name__ == '__main__':
    main()
