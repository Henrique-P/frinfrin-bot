import os
from telegram import Update

STANDARD_MOTD_EN = 'Hello! Send me a Twitter, TikTok, Instagram or Furaffinity link for a preview-able link.\n\nYou can also send me Youtube, Spotify or other links that contains trackers so I can remove them for you.\n\nIf you want to include a tracker pattern in my search please message @Yolfrin.'
STANDARD_MOTD_BR = 'Oi! Me envie um link do Twitter, Tiktok, Instagram ou Furaffinity e eu te devolvo um link com preview.\n\nVocê também pode me enviar links do Youtube, Spotify ou outros links que contém rastreadores e eu os removerei para você.\n\nCaso queira adicionar um rastreador à minha busca contate @Yolfrin.\n\nNota:Tradução PT-BR em andamento.'
MOTD_EN = os.getenv('MOTD', STANDARD_MOTD_EN)
MOTD_BR = os.getenv('MOTD', STANDARD_MOTD_BR)

UNKNOWN_MESSAGE_EN = 'I did not recognize your message as a link. Try sending me a link from Instagram, Twitter, Furaffinity or TikTok and I will embed and/or remove any trackers.'
SAME_LINK_EN = 'Nothing to do with this link.'
INVALID_LINK_EN = 'This link is invalid or the content is private.'

UNKNOWN_MESSAGE_BR = 'Não reconheci sua mensagem como um link. Tente me enviar um link do Instagram, Twitter, Furaffinity ou TikTok e eu colocarei um preview e removerei rastreadores.'
SAME_LINK_BR = 'Nada a fazer aqui.'
INVALID_LINK_BR = 'Esse link é inválido ou o conteúdo é privado.'

responseDict = {'en':{'motd': MOTD_EN, 'invalidLink':INVALID_LINK_EN, 'sameLink':SAME_LINK_EN, 'unknownMessage':UNKNOWN_MESSAGE_EN},'pt':{'motd': MOTD_BR, 'invalidLink':INVALID_LINK_BR, 'sameLink':SAME_LINK_BR,'unknownMessage':UNKNOWN_MESSAGE_BR}}

def getTranslatedMessage(lang:str, context:str):
    if lang.startswith('pt'):
        return responseDict['pt'][context]
    else:
        return responseDict['en'][context]
    
async def sendTranslatedMessage(update:Update, context:str):
    userLang = update.effective_user.language_code
    if userLang.startswith('pt'):
        await update.message.reply_text (responseDict['pt'][context])
    else:
        await update.message.reply_text (responseDict['en'][context])
        
class Responses:
    def __init__(self,lang:str):
        if lang not in responseDict:
            lang = 'en'        
        self.dict = responseDict[lang]
        self.motd = self.dict['motd']
        self.invalidLink = self.dict['invalidLink']
        self.unknownMessage = self.dict['unknownMessage']
        self.sameLink = self.dict['sameLink']
        self.shrug = 'CAACAgEAAxkBAAECSm9mXAHqyk3h8vkRx7ucxyF6qQppkAACuQIAAh9lSEfeZwF56Y_N9DUE'