# (c) @AbirHasan2005
# © https://t.me/DK_BOTZ_PAID Project
# Coded By https://t.me/DKBOTZHELP

import shutil


async def delete_all(root: str):
    """
    Delete a Folder.

    :param root: Pass Folder Path as String.
    """

    try:
        shutil.rmtree(root)
    except Exception as e:
        print(e)
