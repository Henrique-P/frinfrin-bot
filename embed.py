from uuid import uuid4
import requests
import re
from telegram.ext import CallbackContext
from telegram import InlineQueryResultPhoto, InputTextMessageContent, Update
#trackerRegexPattern = r'si=[^&]*&?|igsh=[^&]*&?'
from bot import botStatus

async def twitter(update: Update, context: CallbackContext):
    botStatus.logEvent()
    if update.effective_message:
        postId = update.effective_message.text.split(".com/", 1)[1]
        await update.effective_sender.send_message("https://fixupx.com/" + postId)
        await update.effective_message.delete()
        return
    elif update.inline_query:
        if update.inline_query.query:
            postId = update.inline_query.query.split(".com/", 1)[1]
            answer = [InlineQueryResultPhoto(str(uuid4()), "https://d.fixupx.com/" + postId, "https://d.fixupx.com/" + postId, input_message_content= "https://fixupx.com/" + postId)]
            await update.inline_query.answer(answer)

async def tiktok(update: Update, context: CallbackContext):
    botStatus.logEvent()
    if update.effective_message:
        postId = update.effective_message.text
        if re.search(r'vm\.tiktok\.com/.+|tiktok\.com/t/.+', postId):
            response = requests.get(postId, timeout=1)
            postLink = re.search(r'@[^/]+/video/[0-9]+', response.url)
        else:
            postLink = re.search(r'@[^/]+/video/[0-9]+', postId)
        await update.effective_sender.send_message("https://fixtiktok.com/" + postLink.group())
        await update.effective_message.delete()
    elif update.inline_query:
        if update.inline_query.query:
            postId = update.inline_query.query
            if re.search(r'vm\.tiktok\.com/.+|tiktok\.com/t/.+', postId):
                response = requests.get(postId, timeout=1)
                postLink = re.search(r'@[^/]+/video/[0-9]+', response.url)
            else:
                postLink = re.search(r'@[^/]+/video/[0-9]+', postId)
                answer = [InlineQueryResultPhoto(str(uuid4()), "https://d.fixtiktok.com/" + postId, "https://d.fixtiktok.com/" + postId, input_message_content= "https://fixtiktok.com/" + postId)]
                await update.inline_query.answer(answer)

async def furAffinity(update: Update, context: CallbackContext):
    botStatus.logEvent()
    if update.effective_message:
        postId = update.effective_message.text.split("view/", 1)[1]
        await update.effective_sender.send_message("https://fxfuraffinity.net/view/" + postId)
        await update.effective_message.delete()
        return
    elif update.inline_query:
        if update.inline_query.query:
            postId = update.inline_query.query.split("view/", 1)[1]
            answer = [InlineQueryResultPhoto(str(uuid4()), "https://d.fxfuraffinity.net/view/" + postId, "https://d.fxfuraffinity.net/view/" + postId, input_message_content= "https://fxfuraffinity.net/view/" + postId)]
            await update.inline_query.answer(answer)

async def bsky(update: Update, context: CallbackContext):
    botStatus.logEvent()
    if update.effective_message:
        postId = update.effective_message.text.split("profile/", 1)[1]
        await update.effective_sender.send_message("https://fxbsky.app/profile/" + postId)
        await update.effective_message.delete()
        return
    elif update.inline_query:
        if update.inline_query.query:
            postId = update.inline_query.query.split("profile/", 1)[1]
            answer = [InlineQueryResultPhoto(str(uuid4()), "https://d.fxbsky.app/profile/" + postId, "https://d.fxbsky.app/profile/" + postId, input_message_content= "https://fxbsky.app/profile/" + postId)]
            await update.inline_query.answer(answer)