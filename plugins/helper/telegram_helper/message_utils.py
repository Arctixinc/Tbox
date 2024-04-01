#!/usr/bin/env python3
from pyrogram.enums import ParseMode
from pyrogram.errors import ReplyMarkupInvalid, FloodWait, MessageNotModified, MessageEmpty

from .bot import logger


async def sendMessage(message, text, buttons=None, photo=None, **kwargs):
    try:
        await message.reply(text=text, quote=True, disable_web_page_preview=True, disable_notification=True,
                            reply_markup=buttons, reply_to_message_id=rply.id if (rply := message.reply_to_message) and not rply.text and not rply.caption else None,
                            **kwargs)
    except FloodWait as f:
        logger.warning(str(f))
        await sleep(f.value * 1.2)
        return await sendMessage(message, text, buttons, photo)
    except ReplyMarkupInvalid:
        return await sendMessage(message, text, None, photo)
    except MessageEmpty:
        return await sendMessage(message, text, parse_mode=ParseMode.DISABLED)
    except Exception as e:
        logger.error(format_exc())
        return str(e)


async def editMessage(message, text, buttons=None, photo=None):
    try:
        if message.media:
            return await message.edit_caption(caption=text, reply_markup=buttons)
        await message.edit(text=text, disable_web_page_preview=True, reply_markup=buttons)
    except FloodWait as f:
        logger.warning(str(f))
        await sleep(f.value * 1.2)
        return await editMessage(message, text, buttons, photo)
    except (MessageNotModified, MessageEmpty):
        pass
    except ReplyMarkupInvalid:
        return await editMessage(message, text, None, photo)
    except Exception as e:
        logger.error(str(e))
        return str(e)


async def editReplyMarkup(message, reply_markup):
    try:
        return await message.edit_reply_markup(reply_markup=reply_markup)
    except MessageNotModified:
        pass
    except Exception as e:
        logger.error(str(e))
        return str(e)
