import logging, requests
from re import sub
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Application, MessageHandler, filters, CallbackQueryHandler
from os import getenv
from game import rps, rpsStart
from dotenv import load_dotenv

if 'TOKEN' not in os.environ:
    load_dotenv()

TOKEN = getenv('TOKEN')
WEBHOOK_TOKEN = getenv('WEBHOOK_TOKEN')
WEBHOOK_URL = getenv('WEBHOOK_URL')
PORT = getenv('PORT')
KEY_PATH = getenv('KEY_PATH')
CERT_PATH = getenv('CERT_PATH')

trackerRegexPattern = r'&?si=[^&]*|&?igsh=[^&]*'

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
    
async def twitterHandler(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    if not message:
        return
    postLink = message.split(".com/", 1)[1]
    postLink = postLink.split("?")[0]
    instantViewLink = "https://i.fixupx.com/" + postLink
    if instantViewLink == message:
        #logging.info("¯\\_(ツ)_/¯")
        await update.message.reply_sticker("CAACAgEAAxkBAAECSm9mXAHqyk3h8vkRx7ucxyF6qQppkAACuQIAAh9lSEfeZwF56Y_N9DUE")
        return
    user =  update.effective_user.full_name
    #logging.info("FxTwitter Request by %s", user)
    apiLink = "https://api.fxtwitter.com/" + postLink
    statusCode = requests.get(apiLink).status_code
    if statusCode == 404:
        await update.message.reply_text("This post might be invalid or private.")
    else:
        await update.message.reply_text(instantViewLink)

async def tiktokHandler(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    if not message:
        return
    postLink = message.split(".com/", 1)[1]
    postLink = postLink.split("?")[0]
    finalLink = "https://fixuptiktok.com/" + postLink
    if finalLink == message:
        #logging.info("¯\\_(ツ)_/¯")
        await update.message.reply_sticker("CAACAgEAAxkBAAECSm9mXAHqyk3h8vkRx7ucxyF6qQppkAACuQIAAh9lSEfeZwF56Y_N9DUE")
        return
    user =  update.effective_user.full_name
    #logging.info("FxTikTok Request by %s", user)
    apiLink = "https://api.fxtiktok.com/" + postLink
    statusCode = requests.get(apiLink).status_code
    if statusCode == 404:
        await update.message.reply_text("This post might be invalid or private.")
    else:
        await update.message.reply_text(finalLink)
        
async def instaHandler(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    if not message:
        return
    postLink = message.split(".com/reel/", 1)[1]
    postLink = postLink.split("?")[0]
    finalLink = "https://ddinstagram.com/reel/" + postLink
    if finalLink == message:
        #logging.info("¯\\_(ツ)_/¯")
        await update.message.reply_sticker("CAACAgEAAxkBAAECSm9mXAHqyk3h8vkRx7ucxyF6qQppkAACuQIAAh9lSEfeZwF56Y_N9DUE")
        return
    user =  update.effective_user.full_name
    #logging.info("Instagram Request by %s", user)
    await update.message.reply_text(finalLink)
    
async def start(update: Update, context: CallbackContext) -> None:
    user =  update.effective_user.full_name
    #logging.info("%s started the bot", user)
    await update.message.reply_text("Hello! Send me a Twitter, TikTok or Instagram link.")
    
async def trackerRemovalHandler(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Tracker Found. Here is the clean link:")
    cleanLink = sub(trackerRegexPattern,"", update.message.text)
    if not cleanLink:
        await update.message.reply_text("https://youtu.be/dQw4w9WgXcQ", disable_web_page_preview=True)
        user =  update.effective_user.full_name
        #logging.info("%s got RickRoll'd", user)
    else:
        await update.message.reply_text(cleanLink)
        user =  update.effective_user.full_name
        #logging.info("%s removed a tracker", user)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex(r'(twitter|x)\.com/.+/status/.+'), twitterHandler))
    application.add_handler(MessageHandler(filters.Regex(r'tiktok\.com/@.+/video/.+'), tiktokHandler))
    application.add_handler(MessageHandler(filters.Regex(r'instagram\.com/reel/.+'), instaHandler))
    application.add_handler(MessageHandler(filters.Regex(trackerRegexPattern), trackerRemovalHandler))
    application.add_handler(CommandHandler("rps", rpsStart))
    application.add_handler(CallbackQueryHandler(rps,r'Rock|Paper|Scissors'))    
    application.run_webhook(listen='0.0.0.0', port=PORT, secret_token=WEBHOOK_TOKEN, key=KEY_PATH, cert=CERT_PATH, webhook_url=WEBHOOK_URL+PORT)
    

if __name__ == '__main__':
    main()
