# Bot By https://t.me/DKBOTZ || https://t.me/DK_BOTZ || https://t.me/DKBOTZHELP
# Creadit To My Friend https://t.me/Bot_Magic_World

from pyrogram.types import Message
from typing import Union
import logging
from pyrogram.errors import InputUserDeactivated, FloodWait, UserIsBlocked, PeerIdInvalid

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

######################## Get File ID ################################

def get_file_id(update: Message):
    if update.media:
        for message_type in (
            "photo",
            "animation",
            "audio",
            "document",
            "video",
            "video_note",
            "voice",
            "sticker"
        ):
            obj = getattr(msg, message_type)
            if obj:
                setattr(obj, "message_type", message_type)
                return obj