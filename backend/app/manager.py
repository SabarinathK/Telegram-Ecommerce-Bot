import asyncio
import os
import sys 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_PATH = os.path.join(BASE_DIR, "src")
if SRC_PATH not in sys.path:
    sys.path.append(SRC_PATH)

from telegram_bot import _init_bot,loop,application

asyncio.run_coroutine_threadsafe(_init_bot(), loop)

BOT_APP = application
