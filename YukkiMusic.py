import aiohttp, aiofiles, asyncio, base64, logging
import os, platform, random, re, socket
import sys, time, textwrap

from os import getenv
from io import BytesIO
from time import strftime
from functools import partial
from dotenv import load_dotenv
from datetime import datetime
from pyrogram import filters
from typing import Union, List, Pattern
from logging.handlers import RotatingFileHandler

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_async_

from pyrogram import Client, filters as pyrofl
from pytgcalls import PyTgCalls, filters as pytgfl

from pyrogram import idle, __version__ as pyro_version
from pytgcalls.__version__ import __version__ as pytgcalls_version

from ntgcalls import TelegramServerError
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import (
    ChatAdminRequired,
    FloodWait,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pytgcalls.exceptions import NoActiveGroupCall
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import ChatUpdate, Update, GroupCallConfig
from pytgcalls.types import Call, MediaStream, AudioQuality, VideoQuality

from PIL import Image, ImageDraw, ImageEnhance
from PIL import ImageFilter, ImageFont, ImageOps
from youtubesearchpython.__future__ import VideosSearch

loop = asyncio.get_event_loop()

# Versions Dictionary
__version__ = {
    "ᴜꜱᴇʀʙᴏᴛ": "1.0.0",
    "ᴘʏᴛʜᴏɴ": platform.python_version(),
    "ᴘʏʀᴏɢʀᴀᴍ": pyro_version,
    "ᴘʏᴛɢᴄᴀʟʟꜱ": pytgcalls_version,
}

# Store All Logs
logging.basicConfig(
    format="[%(name)s]:: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    handlers=[
        RotatingFileHandler("logs.txt", maxBytes=(1024 * 1024 * 5), backupCount=10),
        logging.StreamHandler(),
    ],
)

LOGGER = logging.getLogger("USERBOT")

# Config Variables
if os.path.exists("Config.env"):
    load_dotenv("Config.env")

API_ID = int(getenv("API_ID", 0))
API_HASH = getenv("API_HASH", None)
STRING_SESSION = getenv("STRING_SESSION", None)
MONGO_DB_URL = getenv("MONGO_DB_URL", None)
OWNER_ID = int(getenv("OWNER_ID", 0))

# Memory Database
ACTIVE_AUDIO_CHATS = []
ACTIVE_VIDEO_CHATS = []
ACTIVE_MEDIA_CHATS = []

QUEUE = {}

# Command & Callback Handlers
def cdx(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["/", "!", "."])

def cdz(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["", "/", "!", "."])

def rgx(pattern: Union[str, Pattern]):
    return pyrofl.regex(pattern)

bot_owner_only = pyrofl.user(OWNER_ID)

# Userbot Client
app = Client(
    name="Userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=str(STRING_SESSION),
)

call = PyTgCalls(app)
call_config = GroupCallConfig(auto_start=False)

mongo_async_cli = _mongo_async_(MONGO_DB_URL)
mongodb = mongo_async_cli.Badxdb

# Store Start Time
__start_time__ = time.time()

# Start and Run
async def main():
    LOGGER.info("Updating directories...")
    if "cache" not in os.listdir():
        os.mkdir("cache")
    if "downloads" not in os.listdir():
        os.mkdir("downloads")
    for file in os.listdir():
        if file.endswith(".session") or file.endswith(".session-journal"):
            os.remove(file)
    LOGGER.info("Directories updated.")

    LOGGER.info("Checking required variables...")
    if API_ID == 0:
        LOGGER.info("❌ 'API_ID' - Not Found")
        sys.exit()
    if not API_HASH:
        LOGGER.info("❌ 'API_HASH' - Not Found")
        sys.exit()
    if not STRING_SESSION:
        LOGGER.info("❌ 'STRING_SESSION' - Not Found")
        sys.exit()
    if not MONGO_DB_URL:
        LOGGER.info("❌ 'MONGO_DB_URL' - Not Found")
        sys.exit()

    try:
        await mongo_async_cli.admin.command("ping")
    except Exception:
        LOGGER.info("❌ 'MONGO_DB_URL' - Not Valid")
        sys.exit()

    LOGGER.info("Required variables collected.")

    LOGGER.info("Starting userbot...")
    try:
        await app.start()
    except Exception as e:
        LOGGER.info(f"🚫 Userbot Error: {e}")
        sys.exit()

    try:
        await call.start()
    except Exception as e:
        LOGGER.info(f"🚫 PyTgCalls Error: {e}")
        sys.exit()

    # Sending Start Message
    start_message = (
        "🌀 **Userbot Started Successfully!**\n"
        "📅 **Date:** `{}`\n"
        "⏰ **Time:** `{}`\n"
        "⚡ **Powered By:** [Your Userbot](https://github.com/your-repo-link)"
    ).format(
        datetime.now().strftime("%Y-%m-%d"),
        datetime.now().strftime("%H:%M:%S")
    )

    try:
        # Replace 'OWNER_ID' with your Telegram user ID
        await app.send_message(OWNER_ID, start_message)
        LOGGER.info("✅ Start message sent to the owner.")
    except Exception as e:
        LOGGER.info(f"🚫 Failed to send start message: {e}")

    LOGGER.info("Userbot started successfully.")
    await idle()


# Some Required Functions ...!!

def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()


async def paste_queue(content):
    loop = asyncio.get_running_loop()
    link = await loop.run_in_executor(None, partial(_netcat, "ezup.dev", 9999, content))
    return link



def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time





# Mongo Database Functions

chatsdb = mongodb.chatsdb
usersdb = mongodb.usersdb




# Served Chats

async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def get_served_chats() -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})



# Served Users

async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})


#ping

@app.on_message(filters.command("ping", prefixes=["/", "!", "."]) & filters.user(OWNER_ID))
async def ping(client, message):
    start_time = datetime.now()
    reply = await message.reply("🏓 **Pong!**")
    end_time = datetime.now()
    ping_time = (end_time - start_time).microseconds / 1000  # Convert to milliseconds
    await reply.edit(f"🏓 **Pong!**\n💡 **Response Time:** `{ping_time} ms`")

if __name__ == "__main__":
    loop.run_until_complete(main())
    
