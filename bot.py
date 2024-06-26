import logging
import re
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CommandHandler, CallbackContext, Application, MessageHandler, filters, InlineQueryHandler
import os
import dotenv
import userStats
import embed

if 'TOKEN' not in os.environ:
    dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')
WEBHOOK_TOKEN = os.getenv('WEBHOOK_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = os.getenv('PORT')
KEY_PATH = os.getenv('KEY_PATH', None)
CERT_PATH = os.getenv('CERT_PATH', None)
customLog = userStats.UsageStatistics()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    customLog.logEvent()
    await update.message.reply_text("Hello! Send me a Twitter, TikTok, Instagram or Furaffinity link for a preview-able link. You can also send me Youtube, Spotify or other links that contains trackers so I can remove them for you.\nIf you want to include a tracker pattern in my re.search please message @Yolfrin.")
    
async def log(update: Update, context: CallbackContext) -> None:
    response = customLog.getFormattedStatistics()
    await update.message.reply_text(response)
        
async def inlineMessage(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    if not query:
        return
    customLog.logEvent()
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
    answer = [InlineQueryResultArticle(response, title, InputTextMessageContent(response), thumbnail_url=thumbUrl, description='Send embed, trackerless link')]
    await update.inline_query.answer(answer)
        
async def privateMessage(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    if not message:
        return
    customLog.logEvent()
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
