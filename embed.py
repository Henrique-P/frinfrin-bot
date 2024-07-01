import re
import uuid
import requests
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, ReplyParameters
from telegram.ext import CallbackContext

generictrackerPattern = r'si=[^&]+|pp=[^&]+'

twitterPattern = r'(twitter|x)\.com/.+/status/[0-9]+'
twitterInlinePattern = r'.+(twitter|x)\.com/.+/status/[0-9]+'
#tiktokShortPattern = r'vm\.tiktok\.com/[^/]+|tiktok\.com/t/[^/]+'
tiktokFullPattern = r'tiktok\.com/@[^/]+/video/[0-9]+'
tiktokInlinePattern = r'.+tiktok\.com/.+'
tiktokCompletePattern = r'tiktok\.com/@[^/]+/video/[0-9]+|vm\.tiktok\.com/[^/]+|tiktok\.com/t/[^/]+'
instaPattern = r'instagram\.com/reel/.+'
instaInlinePattern = r'.+instagram\.com/reel/.+'
furAffinityPattern = r'furaffinity\.net/view/.+'
furAffinityInlinePattern = r'.+furaffinity\.net/view/.+'

async def twitterHandler(update: Update, context: CallbackContext):
    url = context.match.group()
    decomposedLink = url.split('/')
    response = twitterEmbed(decomposedLink)
    if response:
        await update.message.reply_text(response)
        await update.message.delete()
    else:
        replyParams = ReplyParameters(update.message.id)
        await update.message.reply_text("This URL is either invalid or the content is private.", reply_parameters=replyParams)

async def twitterInlineHandler(update: Update, context: CallbackContext):
    url = re.search(twitterPattern, update.inline_query.query).group()
    decomposedLink = url.split('/')
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
    url = context.match.group()
    if url.startswith('vm'):
        response = requests.get('https://' + url , timeout=1)
    else:
        response = requests.get('https://www.' + url , timeout=1)
    if len(response.history):
        url = re.search(tiktokFullPattern, response.url).group()
    decomposedLink = url.split('/')
    domain = decomposedLink[0]
    userHandle = decomposedLink[1]
    postType = decomposedLink[2]
    postId = decomposedLink[3]
    prefix = 'fixup'
    finalLink = f"{prefix}{domain}/{userHandle}/{postType}/{postId}"
    await update.message.reply_text(finalLink)
    await update.message.delete()

async def tiktokInlineHandler(update: Update, context: CallbackContext):
    matches = re.search(tiktokCompletePattern, update.inline_query.query)
    url = matches.group()
    if url.startswith('vm'):
        response = requests.get('https://' + url , timeout=1)
    else:
        response = requests.get('https://www.' + url , timeout=1)
    if len(response.history):
        url = re.search(tiktokFullPattern, response.url).group()
    decomposedLink = url.split('/')
    domain = decomposedLink[0]
    userHandle = decomposedLink[1]
    postType = decomposedLink[2]
    postId = decomposedLink[3]
    prefix = 'fixup'
    finalLink = f"{prefix}{domain}/{userHandle}/{postType}/{postId}"
    thumbUrl = 'https://cdn.pixabay.com/photo/2021/01/30/06/42/tiktok-5962992_1280.png'
    title = "Post Found"
    description = 'Send this TikTok link!'
    answer = [InlineQueryResultArticle(str(uuid.uuid4()), title, InputTextMessageContent(finalLink), thumbnail_url=thumbUrl, description=description)]
    await update.inline_query.answer(answer)

async def instaHandler(update: Update, context: CallbackContext):
    url = context.match.group()
    decomposedLink = url.split('/')
    domain = decomposedLink[0]
    postType = decomposedLink[1]
    postId = decomposedLink[2]
    #trackers = decomposedLink[3]
    prefix = 'dd'
    finalLink = f"{prefix}{domain}/{postType}/{postId}"
    await update.message.reply_text(finalLink)
    await update.message.delete()

async def instaInlineHandler(update: Update, context: CallbackContext):
    url = re.search(instaPattern, update.inline_query.query).group()
    decomposedLink = url.split('/')
    domain = decomposedLink[0]
    postType = decomposedLink[1]
    postId = decomposedLink[2]
    #trackers = decomposedLink[3]
    prefix = 'dd'
    finalLink = f"{prefix}{domain}/{postType}/{postId}"
    thumbUrl = 'https://img.freepik.com/vetores-gratis/instagram-icone-novo_1057-2227.jpg?w=826&t=st=1719789805~exp=1719790405~hmac=292f586caf30f8fed289446a1b4520bdaed57dfe1de281b38f928ec735dfe041'
    title = "Post Found"
    description = 'Send this Instagram link!'
    answer = [InlineQueryResultArticle(str(uuid.uuid4()), title, InputTextMessageContent(finalLink), thumbnail_url=thumbUrl, description=description)]
    await update.inline_query.answer(answer)

async def furAffinityHandler(update: Update, context: CallbackContext):
    url = context.match.group()
    decomposedLink = url.split('/')
    domain = decomposedLink[0]
    postType = decomposedLink[1]
    postId = decomposedLink[2]
    prefix = 'fx'
    finalLink = f"{prefix}{domain}/{postType}/{postId}"
    await update.message.reply_text(finalLink)
    await update.message.delete()

async def furAffinityInlineHandler(update: Update, context: CallbackContext):
    url = re.search(furAffinityPattern, update.inline_query.query).group()
    decomposedLink = url.split('/')
    domain = decomposedLink[0]
    postType = decomposedLink[1]
    postId = decomposedLink[2]
    prefix = 'fx'
    finalLink = f"{prefix}{domain}/{postType}/{postId}"
    thumbUrl = 'https://logos-world.net/wp-content/uploads/2024/02/FurAffinity-Logo-500x281.png'
    title = "Post Found"
    description = 'Send this FurAffinity link!'
    answer = [InlineQueryResultArticle(str(uuid.uuid4()), title, InputTextMessageContent(finalLink), thumbnail_url=thumbUrl, description=description)]
    await update.inline_query.answer(answer)

# async def genericTracker(update: Update, context: CallbackContext):
#     decomposedLink = context.match.string.split('?')
#     decomposedArguments = decomposedLink[1].split('&')
#     url = decomposedLink[0]
#     decomposedArguments.pop(decomposedArguments.index(context.match.group()))
#     allowedArguments = decomposedArguments
#     if not allowedArguments:
#         await update.message.reply_text(url) 
#     else:
#         url += allowedArguments
#         await update.message.reply_text(url)