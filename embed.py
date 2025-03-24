from uuid import uuid4
import requests
import re
from telegram.ext import CallbackContext
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
#trackerRegexPattern = r'si=[^&]*&?|igsh=[^&]*&?'

async def twitter(update: Update, context: CallbackContext):
    if update.effective_message:
        postId = update.effective_message.text.split(".com/", 1)[1]
        await update.effective_sender.send_message("https://fixupx.com/" + postId)
        await update.effective_message.delete()
        return
    elif update.inline_query:
        if update.inline_query.query:
            postId = update.inline_query.query.split(".com/", 1)[1]
            answer = [InlineQueryResultArticle(str(uuid4()), 'X', InputTextMessageContent("https://fixupx.com/" + postId), thumbnail_url='https://cdn.freelogovectors.net/wp-content/uploads/2023/07/twitter-x-logo-freelogovectors.net_.png')]
            await update.inline_query.answer(answer)

async def tiktok(update: Update, context: CallbackContext):
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
                answer = [InlineQueryResultArticle(str(uuid4()), 'TikTok', InputTextMessageContent("https://fixtiktok.com/" + postId), thumbnail_url='')]
                await update.inline_query.answer(answer)

async def furAffinity(update: Update, context: CallbackContext):
    if update.effective_message:
        postId = update.effective_message.text.split("view/", 1)[1]
        await update.effective_sender.send_message("https://fxfuraffinity.net/view/" + postId)
        await update.effective_message.delete()
        return
    elif update.inline_query:
        if update.inline_query.query:
            postId = update.inline_query.query.split("view/", 1)[1]
            answer = [InlineQueryResultArticle(str(uuid4()), 'FurAffinity', InputTextMessageContent("https://fxfuraffinity.net/view/" + postId), thumbnail_url='')]
            await update.inline_query.answer(answer)

async def bsky(update: Update, context: CallbackContext):
    if update.effective_message:
        postId = update.effective_message.text.split("profile/", 1)[1]
        await update.effective_sender.send_message("https://fxbsky.app/profile/" + postId)
        await update.effective_message.delete()
        return
    elif update.inline_query:
        if update.inline_query.query:
            postId = update.inline_query.query.split("profile/", 1)[1]
            answer = [InlineQueryResultArticle(str(uuid4()), 'X', InputTextMessageContent("https://fxbsky.app/profile/" + postId), thumbnail_url='')]
            await update.inline_query.answer(answer)