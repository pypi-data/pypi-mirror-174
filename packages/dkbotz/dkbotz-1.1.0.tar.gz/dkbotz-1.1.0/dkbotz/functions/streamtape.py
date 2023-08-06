# (c) @AbirHasan2005
# © https://t.me/DK_BOTZ_PAID Project
# Coded By https://t.me/DKBOTZHELP

import aiohttp
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dkbotz import *

STREAMTAPE_API_USERNAME = ""
STREAMTAPE_API_PASS = ""


async def UploadToStreamtape(file: str, editable: Message, file_size: int):
    try:
        async with aiohttp.ClientSession() as session:
            Main_API = "https://api.streamtape.com/file/ul?login={}&key={}"
            hit_api = await session.get(Main_API.format(STREAMTAPE_API_USERNAME, STREAMTAPE_API_PASS))
            json_data = await hit_api.json()
            temp_api = json_data["result"]["url"]
            files = {'file1': open(file, 'rb')}
            response = await session.post(temp_api, data=files)
            data_f = await response.json(content_type=None)
            download_link = data_f["result"]["url"]
            filename = file.split("/")[-1].replace("_", " ")
            text_edit = f"**🥳 Your File is Uploaded to Stream tape! As the file size was greater than 2 GB ☹️**\n\n**File Name:** `{filename}`\n**Size:** `{humanbytes(file_size)}`\n**DL Link:** `{download_link}`"
            await editable.edit(text_edit, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📭 Open Streamtape Link 📤", url=download_link)]]))
    except Exception as e:
        print(f"**Error: {e}**")
        await editable.edit("**Sorry, Something went wrong!**\n\n**Can't Upload to Streamtape. You can report at [Support Group](https://t.me/DK_BOTZ)**\n\n**Error: {e}**")
