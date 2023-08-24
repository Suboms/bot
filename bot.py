from main import *
from forward import *
from telethon import events, TelegramClient
from dotenv import load_dotenv
from telethon.sessions import StringSession
import os

# load_dotenv(dotenv_path="./config.env")
load_dotenv()

API_ID = int(os.getenv("ID"))
phone = str(os.getenv("phone"))
API_HASH = str(os.getenv("HASH"))
OWNER_ID = int(os.getenv("OWNER_ID"))
SESSION_STRING = str(os.getenv("SESSION_STRING"))

session = StringSession(SESSION_STRING)
bot = TelegramClient(session, API_ID, API_HASH)


bot.add_event_handler(start_command, events.NewMessage(pattern="/start"))
bot.add_event_handler(source_channel_command, events.NewMessage(pattern="/source"))
bot.add_event_handler(
    destination_channel_command, events.NewMessage(pattern="/destination")
)
bot.add_event_handler(start_date_command, events.NewMessage(pattern="/datestart"))
bot.add_event_handler(end_date_command, events.NewMessage(pattern="/enddate"))
bot.add_event_handler(settings_command, events.NewMessage(pattern="/settings"))
bot.add_event_handler(help_command, events.NewMessage(pattern="/help"))
bot.add_event_handler(handle_forwarding, events.NewMessage(pattern="/forward"))

bot.start()
bot.run_until_disconnected()
