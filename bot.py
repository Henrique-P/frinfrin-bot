import logging
import requests
from telegram import Update
from telegram.ext import CommandHandler, InlineQueryHandler, CallbackContext, Application, MessageHandler, filters
import os
import dotenv
from botInfo import botInfo
import embed
import json

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
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

botNotes = json.loads(open("bot-text-messages.json", "r").read())

async def start(update: Update, context: CallbackContext) -> None:
    botStatus.logEvent()
    await update.message.reply_text(botNotes["welcomeNote"].format(update.effective_user.first_name))
    
async def help(update: Update, context: CallbackContext) -> None:
    botStatus.logEvent()
    await update.message.reply_text(botNotes["privacyNote"])

async def support(update: Update, context: CallbackContext) -> None:
    botStatus.logEvent()
    await update.message.reply_text(botNotes["helpNote"])
    
async def privacy(update: Update, context: CallbackContext) -> None:
    botStatus.logEvent()
    await update.message.reply_text(botNotes["privacyNote"])

async def log(update: Update, context: CallbackContext) -> None:
    response = botStatus.getFormattedStatistics()
    await update.message.reply_text(response)

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
    application.add_handler(MessageHandler(filters.Regex(r'(twitter|x)\.com/.+/status/\d+') & filters.TEXT & ~filters.COMMAND, embed.twitter))
    application.add_handler(MessageHandler(filters.Regex(r'tiktok\.com/.+') & filters.TEXT & ~filters.COMMAND, embed.tiktok))
    application.add_handler(MessageHandler(filters.Regex(r'bsky\.app/profile/.+') & filters.TEXT & ~filters.COMMAND, embed.bsky))
    application.add_handler(MessageHandler(filters.Regex(r'furaffinity\.net/view/\d+') & filters.TEXT & ~filters.COMMAND, embed.furAffinity))
    application.add_handler(InlineQueryHandler(embed.twitter, r'.+(twitter|x)\.com/.+/status/\d+'))
    application.add_handler(InlineQueryHandler(embed.tiktok, r'.+tiktok\.com/.+'))
    application.add_handler(InlineQueryHandler(embed.bsky, r'.+bsky\.app/profile/.+'))
    application.add_handler(InlineQueryHandler(embed.furAffinity, r'.+furaffinity\.net/view/\d+'))
    if KEY_PATH:
        application.run_webhook(listen='0.0.0.0', port=PORT, secret_token=WEBHOOK_TOKEN, key=KEY_PATH, cert=CERT_PATH, webhook_url=f"{WEBHOOK_URL}:{PORT}")
    else:
        application.run_webhook(listen='0.0.0.0', port=PORT, secret_token=WEBHOOK_TOKEN, webhook_url=f"{WEBHOOK_URL}:{PORT}")

if __name__ == '__main__':
    main()
