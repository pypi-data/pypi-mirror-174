# (c) Shrimadhav U K & @AbirHasan2005
# © https://t.me/DK_BOTZ_PAID Project
# Coded By https://t.me/DKBOTZHELP

import logging
logger = logging.getLogger(__name__)

import asyncio
import os
import time
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

import random




async def generate_screen_shots(video_file, output_directory, no_of_photos, duration):
    images = list()
    ttl_step = duration // no_of_photos
    current_ttl = ttl_step
    for looper in range(no_of_photos):
        await asyncio.sleep(1)
        video_thumbnail = f"{output_directory}/{str(time.time())}.jpg"
        file_generator_command = [
            "ffmpeg",
            "-ss",
            str(round(current_ttl)),
            "-i",
            video_file,
            "-vframes",
            "1",
            video_thumbnail
        ]
        process = await asyncio.create_subprocess_exec(
            *file_generator_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
        print(e_response)
        print(t_response)
        current_ttl += ttl_step
        images.append(video_thumbnail)
    return images


async def screen_shorts_with_metadata(video_file, output_directory, min_duration, no_of_photos):
    metadata = extractMetadata(createParser(video_file))
    duration = 0
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    if duration > min_duration:
        images = []
        ttl_step = duration // no_of_photos
        random_start = random.randint(0, duration - (no_of_photos * ttl_step))
        current_ttl = random_start
        for looper in range(0, no_of_photos):
            ss_img = await take_screen_shot(video_file, output_directory, current_ttl)
            current_ttl = current_ttl + ttl_step
            images.append(ss_img)
        return images
    else:
        return None


#################################################################################################################################################################################################################################################################################################
