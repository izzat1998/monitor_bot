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
    # Splitting the message to get arguments
    args = message.text.split()[1:]

    if len(args) == 0:
        await message.reply("Please provide a service name. Usage: /check_service <service_name>")
        return

    service_name = args[0]

    # Since subprocess.run isn't async, we use run_in_executor to not block the event loop
    result = await asyncio.to_thread(subprocess.run, ['systemctl', 'status', service_name], capture_output=True,
                                     text=True)

    if result.returncode == 0:
        await message.reply(f"{service_name} is active.")
    else:
        await message.reply(f"{service_name} is not active or doesn't exist.")


def register_system_info(dp: Dispatcher):
    dp.register_message_handler(get_system_info, commands=["system_info"], state="*")
    dp.register_message_handler(check_service, commands=["check_service"], state="*")
