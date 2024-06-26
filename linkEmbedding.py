import requests
import re
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from languages import sendTranslatedMessage

trackerRegexPattern = r'si=[^&]*&?|igsh=[^&]*&?'

async def twitter(update: Update):
    message = update.message.text
    postLink = re.search(r'[^/]+/status/[0-9]+', message).group()
    apiLink = "https://api.fxtwitter.com/" + postLink
    statusCode = requests.get(apiLink).status_code
    if statusCode != 200:
        await sendTranslatedMessage(update,'invalidLink')
        return
    response = "https://fixupx.com/" + postLink
    if response == message:
        await sendTranslatedMessage(update,'sameLink')
        await update.message.reply_sticker("CAACAgEAAxkBAAECSm9mXAHqyk3h8vkRx7ucxyF6qQppkAACuQIAAh9lSEfeZwF56Y_N9DUE")
        return
    await update.message.reply_text(response)

async def inlineTwitter(update: Update):
    message = update.inline_query.query
    postLink = re.search(r'[^/]+/status/[0-9]+', message).group()
    apiLink = "https://api.fxtwitter.com/" + postLink
    statusCode = requests.get(apiLink).status_code
    response = "https://fixupx.com/" + postLink
    if statusCode != 200:
        return
    thumbUrl = 'https://cdn.freelogovectors.net/wp-content/uploads/2023/07/twitter-x-logo-freelogovectors.net_.png'
    title = "X"
    await update.inline_query.answer([InlineQueryResultArticle(response, title, InputTextMessageContent(response), thumbnail_url=thumbUrl, description='Send embed, trackerless link')])

async def tiktok(update: Update):
    message = update.message.text
    if re.search(r'vm\.tiktok\.com/.+|tiktok\.com/t/.+',message):
        response = requests.get(message)
        postLink = re.search(r'@[^/]+/video/[0-9]+', response.url)
    else:
        postLink = re.search(r'@[^/]+/video/[0-9]+', message)
    if not postLink:
        await sendTranslatedMessage(update,'invalidLink')
        return
    response = "https://fixuptiktok.com/" + postLink.group()
    await update.message.reply_text(response)

async def inlineTiktok(update: Update):
    message = update.inline_query.query
    if re.search(r'vm\.tiktok\.com/.+|tiktok\.com/t/.+',message):
        response = requests.get(message)
        postLink = re.search(r'@[^/]+/video/[0-9]+', response.url)
    else:
        postLink = re.search(r'@[^/]+/video/[0-9]+', message)
    if not postLink:
        return
    thumbUrl = ''
    title = "TikTok"
    await update.inline_query.answer([InlineQueryResultArticle(response, title, InputTextMessageContent(response), thumbnail_url=thumbUrl, description='Send embed, trackerless link')])

async def insta(update: Update):
    message = update.message.text
    postLink = message.split(".com/reel/", 1)[1]
    postLink = postLink.split("?")[0]
    response = "https://ddinstagram.com/reel/" + postLink
    await update.message.reply_text(response)
    
async def inlineInsta(update: Update):
    message = update.inline_query.query
    postLink = message.split(".com/reel/", 1)[1]
    postLink = postLink.split("?")[0]
    response = "https://ddinstagram.com/reel/" + postLink
    thumbUrl = ''
    title = "Instagram"
    await update.inline_query.answer([InlineQueryResultArticle(response, title, InputTextMessageContent(response), thumbnail_url=thumbUrl, description='Send embed, trackerless link')])

async def furAffinity(update: Update):
    message = update.message.text
    postLink = message.split(".net/view/", 1)[1]
    response = "https://www.fxfuraffinity.net/view/" + postLink
    await update.message.reply_text(response)

async def inlineFurAffinity(update: Update):
    message = update.inline_query.query
    postLink = message.split(".net/view/", 1)[1]
    response = "https://www.fxfuraffinity.net/view/" + postLink
    thumbUrl = 'https://logos-world.net/wp-content/uploads/2024/02/FurAffinity-Logo-500x281.png'
    title = "FurAffinity"
    await update.inline_query.answer([InlineQueryResultArticle(response, title, InputTextMessageContent(response), thumbnail_url=thumbUrl, description='Send embed, trackerless link')])

async def trackerRemoval(update:Update):
    message = update.message.text
    cleanLink = re.sub(trackerRegexPattern,"", message)
    response = re.sub(r'\?$','', cleanLink)
    await update.message.reply_text(response)

async def inlineTrackerRemoval(update:Update):
    message = update.inline_query.query
    cleanLink = re.sub(trackerRegexPattern,"", message)
    response = re.sub(r'\?$','', cleanLink)
    thumbUrl = ''
    title = "Tracker Removed"
    await update.inline_query.answer([InlineQueryResultArticle(response, title, InputTextMessageContent(response), thumbnail_url=thumbUrl, description='Send embed, trackerless link')])