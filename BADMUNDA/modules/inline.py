import asyncio
from pyrogram import Client, InlineQueryResultPhoto, InlineQueryResultArticle, InlineKeyboardMarkup, InputTextMessageContent
from BADMUNDA.modules.buttons import paginate_plugins
from BADMUNDA.modules.wrapper import inline_wrapper
from pyrogram.types import InlineQuery
from yu import __version__

async def help_menu_logo(answer):
    image = None
    thumb_image = image or "https://telegra.ph/file/3063af27d9cc8580845e1.jpg"
    button = paginate_plugins(0, plugs, "help")
    
    answer.append(
        InlineQueryResultPhoto(
            photo_url=thumb_image,
            title="💫 ʜᴇʟᴘ ᴍᴇɴᴜ  ✨",
            thumb_url=thumb_image,
            description="🥀 Open Help Menu Of PBXUSERBOT ✨...",
            caption=f"""
**💫 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʜᴇʟᴘ ᴍᴇɴᴜ ᴏᴘ.
ᴘʙx ᴜsᴇʀʙᴏᴛ  » {__version__} ✨

❤️ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ
ɢᴇᴛ ᴜsᴇʀʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs ❤️

🌹ᴘᴏᴡᴇʀᴇᴅ ʙʏ ☆  [ ᴘʙx ᴜᴘᴅᴀᴛᴇ ](https://t.me/HEROKUBIN_01) 🌹**
""",
            reply_markup=InlineKeyboardMarkup(button),
        )
    )
    return answer


async def help_menu_text(answer):
    button = paginate_plugins(0, plugs, "help")
    
    answer.append(
        InlineQueryResultArticle(
            title="💫 ʜᴇʟᴘ ᴍᴇɴᴜ  ✨",
            input_message_content=InputTextMessageContent(f"""
**💫 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʜᴇʟᴘ ᴍᴇɴᴜ ᴏᴘ.
ᴘʙx ᴜsᴇʀʙᴏᴛ  » {__version__} ✨

❤️ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ
ɢᴇᴛ ᴜsᴇʀʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs ❤️

🌹ᴘᴏᴡᴇʀᴇᴅ ʙʏ ☆  [ ᴘʙx ᴜᴘᴅᴀᴛᴇ ](https://t.me/HEROKUBIN_01) 🌹**
""", disable_web_page_preview=True),
            reply_markup=InlineKeyboardMarkup(button),
        )
    )
    return answer


async def run_async_inline():
    @bot.on_inline_query()
    @inline_wrapper
    async def inline_query_handler(bot, query: InlineQuery):
        text = query.query
        answer = []

        if text.startswith("help_menu_logo"):
            answer = await help_menu_logo(answer)
        elif text.startswith("help_menu_text"):
            answer = await help_menu_text(answer)
        
        if answer:
            try:
                await bot.answer_inline_query(query.id, results=answer, cache_time=10)
            except Exception as e:
                print(f"Error answering inline query: {e}")
