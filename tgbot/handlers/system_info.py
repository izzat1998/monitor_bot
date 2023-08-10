import psutil as psutil
from aiogram import Dispatcher
from aiogram.types import Message


async def get_system_info(message: Message):
    cpu_percent = psutil.cpu_percent()
    mem_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    text = f"""*CPU usage*: {cpu_percent}%
*Memory usage*: {mem_info.percent}%
*Disk usage*: {disk_usage.percent}%"""

    await message.reply(text, parse_mode='Markdown')


def register_system_info(dp: Dispatcher):
    dp.register_message_handler(get_system_info, commands=["system_info"], state="*")
