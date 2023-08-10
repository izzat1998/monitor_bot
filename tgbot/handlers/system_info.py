import asyncio
import subprocess

import psutil as psutil
from aiogram import Dispatcher, types
from aiogram.types import Message


async def get_system_info(message: Message):
    cpu_percent = psutil.cpu_percent()
    mem_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    text = f"""*CPU usage*: {cpu_percent}%
*Memory usage*: {mem_info.percent}%
*Disk usage*: {disk_usage.percent}%"""

    await message.reply(text, parse_mode='Markdown')


async def check_service(message: types.Message):
    SERVICES = ['order', 'celery', 'telegram_bot', 'redis', 'image']
    TEXT = """"""
    # Splitting the message to get arguments
    # Since subprocess.run isn't async, we use run_in_executor to not block the event loop
    for service_name in SERVICES:
        TEXT += f"{service_name}: {await asyncio.to_thread(subprocess.run, ['systemctl', 'status', service_name], capture_output=True, text=True)}\n"

    await message.answer(TEXT)


def register_system_info(dp: Dispatcher):
    dp.register_message_handler(get_system_info, commands=["system_info"], state="*")
    dp.register_message_handler(check_service, commands=["check_service"], state="*")
