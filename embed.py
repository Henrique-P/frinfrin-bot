import requests
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CallbackContext

trackerRegexPattern = r'si=[^&]*&?|igsh=[^&]*&?'

async def twitter(update: Update, context: CallbackContext):
    decomposed = context.match.group().split('/')
    domain = decomposed[0]
    userHandle = decomposed[1]
    postId = decomposed[3]
    if domain == 'x.com':
        prefix = 'fixup'
    else:
        prefix = 'fx'
    apiLink = f"https://api.fxtwitter.com/{userHandle}/status/{postId}"
    composed = f"{prefix}{domain}/{userHandle}/status/{postId}"
    isPostOK = requests.get(apiLink).status_code == 200
    if update.inline_query:
        if not isPostOK:
            return
        thumbUrl = 'https://cdn.freelogovectors.net/wp-content/uploads/2023/07/twitter-x-logo-freelogovectors.net_.png'
        title = "Post Found"
        description = 'Send this Twitter link!'
        answer = [InlineQueryResultArticle(composed, title, InputTextMessageContent(composed), thumbnail_url=thumbUrl, description=description)]
        await update.inline_query.answer(answer)
    elif update.message.text:
        if not isPostOK:
            await update.message.reply_text("This URL is either invalid or the content is private.")
        else:
            await update.message.reply_text(composed)

def tiktok(update: Update, context: CallbackContext):
    if re.search(r'vm\.tiktok\.com/.+|tiktok\.com/t/.+',originalLink):
        response = requests.get(originalLink)
        postLink = re.search(r'@[^/]+/video/[0-9]+', response.url)
    else:
        postLink = re.search(r'@[^/]+/video/[0-9]+', originalLink)
    if not postLink:
        return -1
    return "https://fixuptiktok.com/" + postLink.group()

def insta(update: Update, context: CallbackContext):
    postLink = originalLink.split(".com/reel/", 1)[1]
    postLink = postLink.split("?")[0]
    finalLink = "https://ddinstagram.com/reel/" + postLink
    return finalLink

def furAffinity(update: Update, context: CallbackContext):
    postLink = originalLink.split(".net/view/", 1)[1]
    finalLink = "https://www.fxfuraffinity.net/view/" + postLink
    return finalLink

def trackerRemoval(update: Update, context: CallbackContext):
    cleanLink = re.sub(trackerRegexPattern,"", originalLink)
    cleanLink = re.sub(r'\?$','', cleanLink)
    return cleanLink