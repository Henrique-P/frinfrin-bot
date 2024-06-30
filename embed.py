import re
import uuid
import requests
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CallbackContext

trackerRegexPattern = r'si=[^&]*&?|igsh=[^&]*&?'

twitterPattern = r'(twitter|x)\.com/.+/status/[0-9]+'
twitterInlinePattern = r'.+(twitter|x)\.com/.+/status/[0-9]+'
tiktokShortenedPattern = r'vm\.tiktok\.com/[^/]+|tiktok\.com/t/[^/]+'
tiktokFullPattern = r'tiktok\.com/@[^/]+/video/[0-9]+'
tiktokInlinePattern = r'.+tiktok\.com/.+'
instaPattern = r'instagram\.com/reel/.+'
instaInlinePattern = r'.+instagram\.com/reel/.+'
furAffinityPattern = r'furaffinity\.net/view/.+'
furAffinityInlinePattern = r'.+furaffinity\.net/view/.+'

async def twitterHandler(update: Update, context: CallbackContext):
    decomposedLink = context.match.group().split('/')
    response = twitterEmbed(decomposedLink)
    if response:
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("This URL is either invalid or the content is private.")

async def twitterInlineHandler(update: Update, context: CallbackContext):
    #decomposedLink = context.match.re.search(twitterPattern).group().split('/')
    decomposedLink = re.search(twitterPattern, update.inline_query.query).group().split('/')
    response = twitterEmbed(decomposedLink)
    if response:
        thumbUrl = 'https://cdn.freelogovectors.net/wp-content/uploads/2023/07/twitter-x-logo-freelogovectors.net_.png'
        title = "Post Found"
        description = 'Send this Twitter link!'
        answer = [InlineQueryResultArticle(str(uuid.uuid4()), title, InputTextMessageContent(response), thumbnail_url=thumbUrl, description=description)]
        await update.inline_query.answer(answer)

def twitterEmbed(link:str):
    domain = link[0]
    userHandle = link[1]
    postId = link[3]
    if domain == 'x.com':
        prefix = 'fixup'
    else:
        prefix = 'fx'
    apiLink = f"https://api.fxtwitter.com/{userHandle}/status/{postId}"
    composed = f"{prefix}{domain}/{userHandle}/status/{postId}"
    isPostOK = requests.get(apiLink).status_code == 200
    if isPostOK:
        return composed

async def tiktokHandler(update: Update, context: CallbackContext):
    match = context.match
    pass
    # response = requests.get(originalLink, timeout=1)
    # postLink = re.search(r'@[^/]+/video/[0-9]+', response.url)
    # else:
    #     postLink = re.search(r'@[^/]+/video/[0-9]+', originalLink)
    # if not postLink:
    #     return -1
    # return "https://fixuptiktok.com/" + postLink.group()

async def instaHandler(update: Update, context: CallbackContext):
    decomposedLink = context.match.group().split('/')
    domain = decomposedLink[0]
    postType = decomposedLink[1]
    postId = decomposedLink[2]
    #trackers = decomposedLink[3]
    prefix = 'dd'
    finalLink = f"{prefix}{domain}/{postType}/{postId}"
    await update.message.reply_text(finalLink)

async def furAffinityHandler(update: Update, context: CallbackContext):
    decomposedLink = context.match.group().split('/')
    domain = decomposedLink[0]
    postType = decomposedLink[1]
    postId = decomposedLink[2]
    prefix = 'fx'
    finalLink = f"{prefix}{domain}/{postType}/{postId}"
    await update.message.reply_text(finalLink)