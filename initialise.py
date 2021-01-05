from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import API_TOKEN


API_TOKEN = API_TOKEN
bot = Bot(token=API_TOKEN)
print(f"API_TOKEN={API_TOKEN}")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

