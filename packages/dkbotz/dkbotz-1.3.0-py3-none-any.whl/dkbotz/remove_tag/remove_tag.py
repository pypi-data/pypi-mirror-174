import pyrogram
import os
from pyrogram import Client as dkbotz, filters
from pyrogram.types import Message, User

#Creadit :- @DKBOTZ And @bughunter0


#@dkbotz.on_message(filters.forwarded & filters.channel)
async def removetag(bot, message):
   try:
       chat_id = message.chat.id
       forward_msg = await message.copy(chat_id)
       await message.delete()
   except:
       await message.reply_text("Oops , Recheck My Admin Permissions & Try Again")
    
