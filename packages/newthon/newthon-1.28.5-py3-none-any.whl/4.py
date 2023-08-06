from telethon.sync import TelegramClient
from telethon import functions, types, events 
import logging 
import asyncio
import asyncio


import sys

id = 12968842

hash = '6cd02ff1e2d35dd1ec7fd25d06a17c93'


client = TelegramClient('disknull.session', id, hash)

get = client.get_messages

en = client.get_entity

co = client.connect()

dis = client.disconnect()

me = "me"

chat = types.PeerChannel(1397662696)

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

print(f"\x1b[6;14;132m\x1b[6;14;40m")

# logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)
logging.basicConfig(stream=sys.stdout, format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.DEBUG)

#!NULL____ 
# client.connect()

print(f"\x1b[6;14;132m\x1b[6;14;40m")

client.start()

def raw(cock=None):
    @client.on(events.Raw(cock))
    async def c(e):
        print(e.stringify())
    client.run_until_disconnected()


# captchaBtn = msg.buttons[0][0].button

# req = client(functions.messages.RequestUrlAuthRequest(
# peer=msg.chat_id,
# msg_id=msg.id,
# button_id=captchaBtn.button_id,
# url=captchaBtn.url))

# if isinstance(req, types.UrlAuthResultAccepted):
    # finalUrl = req.url

# elif isinstance(req, types.UrlAuthResultRequest):
    # req2 = client(functions.messages.AcceptUrlAuthRequest(write_allowed=True, 
            # peer=msg.chat_id,
            # msg_id=msg.id,
            # button_id=captchaBtn.button_id 
        # ))
    # finalUrl = req2.url


client.run_until_disconnected()
