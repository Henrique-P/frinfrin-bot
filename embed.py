import requests
import re

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update

#trackerRegexPattern = r'si=[^&]*&?|igsh=[^&]*&?'

def twitter(update: Update):
    if update.message == True:
        postId = update.message.text.split(".com/status/", 1)[1]
    elif update.channel_post == True:
        postId = update.channel_post.text.split(".com/status/", 1)[1]
    elif update.inline_query == True:
        postId = update.inline_query.query.split(".com/status/", 1)[1]    
    return "https://fixupx.com/" + postId

# def tiktok(originalLink: str):
#     if re.search(r'vm\.tiktok\.com/.+|tiktok\.com/t/.+',originalLink):
#         response = requests.get(originalLink, timeout=1)
#         postLink = re.search(r'@[^/]+/video/[0-9]+', response.url)
#     else:
#         postLink = re.search(r'@[^/]+/video/[0-9]+', originalLink)
#     if not postLink:
#         return -1
#     return "https://fixuptiktok.com/" + postLink.group()

# def insta(originalLink: str):
#     postLink = originalLink.split(".com/reel/", 1)[1]
#     postLink = postLink.split("?")[0]
#     finalLink = "https://ddinstagram.com/reel/" + postLink
#     return finalLink

# def furAffinity(originalLink: str):
#     postLink = originalLink.split(".net/view/", 1)[1]
#     finalLink = "https://www.fxfuraffinity.net/view/" + postLink
#     return finalLink

# def bsky(originalLink: str):
#     postLink = originalLink.split(".app/profile/", 1)[1]
#     finalLink = "https://fxbsky.app/profile/" + postLink
#     return finalLink

# def trackerRemoval(originalLink: str):
#     cleanLink = re.sub(trackerRegexPattern,"", originalLink)
#     cleanLink = re.sub(r'\?$','', cleanLink)
#     return cleanLink