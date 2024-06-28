# frinfrin-bot
<img src="https://healthchecks.io/badge/23227592-d434-4fe4-9fb2-c9a4e7/H_EPQhcZ-2.svg" alt="healthchecks.io">
https://python-telegram-bot.org

This is a telegram bot that accepts links via direct message or online mode and embeds them using known services(eg. fxtwitter). It also removes trackers.

For local runs it's necessary to setup a env file and create SSL keys.

Necessary ENV Constants:
TOKEN - The Telegram Api Token.
WEBHOOK_TOKEN - The webhook token to be used by run_webhook().
WEBHOOK_URL - The bot URL(DDNS).
PORT - The port for receiving webhooks from Telegram API.
KEY_PATH - the SSL key path.
CERT_PATH - the SSL cert path.
