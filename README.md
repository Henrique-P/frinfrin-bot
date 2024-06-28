# frinfrin-bot
<img src="https://healthchecks.io/badge/23227592-d434-4fe4-9fb2-c9a4e7/H_EPQhcZ-2.svg" alt="healthchecks.io">
This is a telegram bot that accepts links via direct message or online mode and embeds them using known services(eg. fxtwitter). It also removes trackers.
This bot uses the Python-Telegram-Bot library.
For local runs it's necessary to setup a env file and create SSL keys.

Template for .env file:

TOKEN=telegramToken
WEBHOOK_TOKEN=secret_word
WEBHOOK_URL=url-here:
PORT=1234
KEY_PATH=ssl\key.key
CERT_PATH=ssl\cert.pem
