import requests
from re import sub

trackerRegexPattern = r'si=[^&]*&?|igsh=[^&]*&?'

def twitter(originalLink: str):
    postLink = originalLink.split(".com/", 1)[1]
    postLink = postLink.split("?")[0]
    instantViewLink = "https://i.fixupx.com/" + postLink
    apiLink = "https://api.fxtwitter.com/" + postLink
    statusCode = requests.get(apiLink).status_code
    if statusCode == 404:
        return -1
    else:
        return instantViewLink

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
    cleanLink = sub(trackerRegexPattern,"", originalLink)
    cleanLink = sub(r'\?$','', cleanLink)
    return cleanLink