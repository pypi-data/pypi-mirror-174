# Bot By https://t.me/DKBOTZ || https://t.me/DK_BOTZ || https://t.me/DKBOTZHELP
# Creadit To My Friend https://t.me/Bot_Magic_World



import time


GAP = {}

TIME_GAP =  1

async def CheckTimeGap(user_id: int):
    """A Function for checking user time gap!
    :parameter user_id Telegram User ID"""

    if str(user_id) in GAP:
        current_time = time.time()
        previous_time = GAP[str(user_id)]
        if round(current_time - previous_time) < TIME_GAP:
            return True, round(previous_time - current_time + TIME_GAP)
        elif round(current_time - previous_time) >= TIME_GAP:
            del GAP[str(user_id)]
            return False, None
    elif str(user_id) not in GAP:
        GAP[str(user_id)] = time.time()
        return False, None
