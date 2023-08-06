# (c) Shrimadhav U K & @AbirHasan2005
# © https://t.me/DK_BOTZ_PAID Project
# Coded By https://t.me/DKBOTZHELP

import asyncio
import os
import time
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery




async def cult_small_video(video_file, output_directory, start_time, end_time, format_):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + str(round(time.time())) + "." + format_.lower()
    file_generator_command = [
        "ffmpeg",
        "-i",
        video_file,
        "-ss",
        str(start_time),
        "-to",
        str(end_time),
        "-async",
        "1",
        "-strict",
        "-2",
        out_put_file_name
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
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None


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
