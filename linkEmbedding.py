import requests
import re

trackerRegexPattern = r'si=[^&]*&?|igsh=[^&]*&?'

def twitter(originalLink: str):
    postLink = re.search(r'[^/]+/status/[0-9]+', originalLink).group()
    apiLink = "https://api.fxtwitter.com/" + postLink
    statusCode = requests.get(apiLink).status_code
    if statusCode != 200:
        return -1
    else:
        return "https://fixupx.com/" + postLink

def tiktok(originalLink: str):
    if originalLink.find('vm.') != -1 or originalLink.find('com/t/') != -1:
        response = requests.get(originalLink)
        if response.history:
            hydratedLink = response.url
        else:
            return -1
    else:
        hydratedLink = originalLink
    postLink = hydratedLink.split(".com/", 1)[1]
    postLink = postLink.split("?")[0]
    finalLink = "https://fixuptiktok.com/" + postLink
    return finalLink

def insta(originalLink: str):
    postLink = originalLink.split(".com/reel/", 1)[1]
    postLink = postLink.split("?")[0]
    finalLink = "https://ddinstagram.com/reel/" + postLink
    return finalLink

def furAffinity(originalLink: str):
    postLink = originalLink.split(".net/view/", 1)[1]
    finalLink = "https://www.fxfuraffinity.net/view/" + postLink
    return finalLink

def trackerRemoval(originalLink: str):
    cleanLink = re.sub(trackerRegexPattern,"", originalLink)
    cleanLink = re.sub(r'\?$','', cleanLink)
    return cleanLink