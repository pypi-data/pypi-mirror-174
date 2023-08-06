# Bot By https://t.me/DKBOTZ || https://t.me/DK_BOTZ || https://t.me/DKBOTZHELP
# Creadit To My Friend https://t.me/Bot_Magic_World


import logging
logger = logging.getLogger(__name__)

import os
import time
import random
import asyncio
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser


#################################################################################################################################################################################################################################################################################################

async def take_screen_shot(video_file, output_directory, ttl):

    out_put_file_name = output_directory + "/" + str(time.time()) + ".jpg"
    file_genertor_command = ["ffmpeg", "-ss", str(ttl), "-i", video_file, "-vframes", "1", out_put_file_name]

    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None


