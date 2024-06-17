import os
import django
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Создаем бота и диспетчера
bot = Bot(token='6732276189:AAF_ZMJNM0FFRK3TQYgSAF3NdCdHJw-EsbE')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
