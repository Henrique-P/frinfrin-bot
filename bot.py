import logging
import re
import requests
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CommandHandler, CallbackContext, Application, MessageHandler, filters, InlineQueryHandler
import os
import dotenv
from botInfo import botInfo
import embed
from uuid import uuid4

if 'TOKEN' not in os.environ:
    dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')
WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = os.getenv('PORT')
KEY_PATH = os.getenv('KEY_PATH')
CERT_PATH = os.getenv('CERT_PATH')
PING_URL = os.getenv('PING_URL')

botStatus = botInfo()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARN
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    botStatus.logEvent()
    await update.message.reply_text(f"Hello, {update.effective_user.first_name}!\nSee /support for all the supported medias.\nFor use help, click here: /help\nYou can also check this channel if you want to know more about this bot's development:\nhttps://t.me/FrinFrinNews")
    
async def help(update: Update, context: CallbackContext) -> None:
    botStatus.logEvent()
    await update.message.reply_text("Alrighty. Lets walk you through this scenario: You were browsing twitter and sent your friend this post:\nhttps://twitter.com/FopsHourly/status/1806281425915883661")
    await update.message.reply_text("Notice that despite the content being a video, twitter only allows you both to preview a static frame of the video. Now lets try using a service to embed the video in this link:\nhttps://fxtwitter.com/FopsHourly/status/1806281425915883661")
    await update.message.reply_text("Much better, right? Now you can try sending me a link for one of the supported social medias and I'll reply to you with the embedded link.\nFor full functionality guide or suggestions please contact @Yolfrin anytime.")

async def support(update: Update, context: CallbackContext) -> None:
    botStatus.logEvent()
    await update.message.reply_text("Currently supported platforms for embedding are: Twitter, TikTok, Instagram and Furaffinity.\nI can also remove URL trackers from Spotify and Youtube links.")
    
async def privacy(update: Update, context: CallbackContext) -> None:
    botStatus.logEvent()
    await update.message.reply_text("This bot keeps no data about how you use it. No user data, links or messages are logged.\nThis bot does not have ANY association with the people responsible for the embedding services used.")

async def log(update: Update, context: CallbackContext) -> None:
    response = botStatus.getFormattedStatistics()
    await update.message.reply_text(response)
        
async def inlineMessage(update: Update, context: CallbackContext) -> None:
    if not update.inline_query.query:
        return
    query = update.inline_query.query
    botStatus.logEvent()
    if re.search(r'(twitter|x)\.com/.+/status/[0-9]+',query):
        response = embed.twitter(query)
        thumbUrl = 'https://cdn.freelogovectors.net/wp-content/uploads/2023/07/twitter-x-logo-freelogovectors.net_.png'
        title = "X"
    elif re.search(r'tiktok\.com/.+',query):
        response = embed.tiktok(query)
        thumbUrl = ''
        title = "TikTok"
    elif re.search(r'instagram\.com/reel/.+', query):
        response = embed.insta(query)
        thumbUrl = ''
        title = "Instagram"
    elif re.search(r'furaffinity\.net/view/.+', query):
        response = embed.furAffinity(query)
        thumbUrl = 'https://logos-world.net/wp-content/uploads/2024/02/FurAffinity-Logo-500x281.png'
        title = "FurAffinity"
    elif re.search(embed.trackerRegexPattern, query):
        response = embed.trackerRemoval(query)
        thumbUrl = ''
        title = "Tracker Removed"
    else:
        return
    if not response or response == -1 or response == query:
        return
    answer = [InlineQueryResultArticle(str(uuid4()), title, InputTextMessageContent(response), thumbnail_url=thumbUrl, description='Send embed, trackerless link')]
    await update.inline_query.answer(answer)
        
async def privateMessage(update: Update, context: CallbackContext) -> None:
    if not update.message.text:
        return
    botStatus.logEvent()
    message = update.message.text
    if re.search(r'(twitter|x)\.com/.+/status/[0-9]+', message):
        response = embed.twitter(message)
    elif re.search(r'tiktok\.com/.+', message):
        response = embed.tiktok(message)
    elif re.search(r'instagram\.com/reel/.+', message):
        response = embed.insta(message)
    elif re.search(r'furaffinity\.net/view/.+', message):
        response = embed.furAffinity(message)
    elif re.search(embed.trackerRegexPattern, message):
        response = embed.trackerRemoval(message)
    else:
        await update.message.reply_text("Message not recognized. Try sending me a Instagram, Twitter, Furaffinity or TikTok link and I will embed and/or remove any trackers.")
        return
    if message == response:
        await update.message.reply_text("Nothing to do with this link.")
        await update.message.reply_sticker("CAACAgEAAxkBAAECSm9mXAHqyk3h8vkRx7ucxyF6qQppkAACuQIAAh9lSEfeZwF56Y_N9DUE")
        return
    elif not response:
        await update.message.reply_text("Here's your link:\nhttps://youtu.be/dQw4w9WgXcQ", disable_web_page_preview=True)
        return
    elif response == -1:
        await update.message.reply_text("This URL is either invalid or the content is private.")
        return
    await update.message.reply_text(response)
    await update.message.delete()

async def healthPing(context: CallbackContext):
    requests.get(PING_URL, timeout=1)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    if PING_URL:
            application.job_queue.run_repeating(healthPing, interval=60, first=10)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("support", support))
    application.add_handler(CommandHandler("log", log))
    application.add_handler(CommandHandler("privacy", privacy))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, privateMessage))
    application.add_handler(InlineQueryHandler(inlineMessage))
    if not KEY_PATH:
        application.run_webhook(listen='0.0.0.0', port=PORT, secret_token=WEBHOOK_TOKEN, webhook_url=f"{WEBHOOK_URL}:{PORT}")
    else:
        application.run_webhook(listen='0.0.0.0', port=PORT, secret_token=WEBHOOK_TOKEN, key=KEY_PATH, cert=CERT_PATH, webhook_url=f"{WEBHOOK_URL}:{PORT}")

if __name__ == '__main__':
    main()
