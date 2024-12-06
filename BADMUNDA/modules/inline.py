import asyncio
from pyrogram.types import InlineQueryResultCachedPhoto, InlineQueryResultArticle, InlineKeyboardMarkup, InputTextMessageContent

from BADMUNDA.modules.buttons import *
from BADMUNDA.modules.wrapper import *
from pyrogram.types import InlineQuery
from YukkiMusic import __version__

async def help_menu_logo(answer):
    thumb_image = "https://telegra.ph/file/3063af27d9cc8580845e1.jpg"
    # Upload the image once to get a `file_id`, then replace `thumb_image` with the actual `file_id` in production.
    button = paginate_plugins(0, plugs, "help")
    
    answer.append(
        InlineQueryResultArticle(
            title="💫 ʜᴇʟᴘ ᴍᴇɴᴜ  ✨",
            input_message_content=InputTextMessageContent(
                f"""
**💫 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ʜᴇʟᴘ ᴍᴇɴᴜ ᴏᴘ.
ᴘʙx ᴜsᴇʀʙᴏᴛ  » {__version__} ✨

❤️ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ
ɢᴇᴛ ᴜsᴇʀʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs ❤️

🌹ᴘᴏᴡᴇʀᴇᴅ ʙʏ ☆  [ ᴘʙx ᴜᴘᴅᴀᴛᴇ ](https://t.me/HEROKUBIN_01) 🌹**
""",
                disable_web_page_preview=True
            ),
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
