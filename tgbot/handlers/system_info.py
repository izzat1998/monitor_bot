import asyncio
import subprocess

import psutil as psutil
from aiogram import Dispatcher, types
from aiogram.types import Message

from tgbot.keyboards.reply import service_keyboard


async def get_system_info(message: Message):
    cpu_percent = psutil.cpu_percent()
    mem_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')
    text = f"""*CPU usage*: {cpu_percent}%
*Memory usage*: {mem_info.percent}%
*Disk usage*: {disk_usage.percent}%"""

    await message.reply(text, parse_mode='Markdown')


async def check_service(message: types.Message):
    SERVICES = ['order', 'celery', 'image', 'telegram_bot', 'redis']
    TEXT = """"""
    # Splitting the message to get arguments
    # Since subprocess.run isn't async, we use run_in_executor to not block the event loop
    for service_name in SERVICES:
        result = await asyncio.to_thread(subprocess.run, ['systemctl', 'status', service_name], capture_output=True,
                                         text=True)
        if result.returncode == 0:
            status = "is currently <b>running</b>"
        elif result.returncode == 1:
            status = "is currently <b>stopped,error occured</b>"
        elif result.returncode == 2:
            status = "is loaded, but <b>stopped</b>"
        elif result.returncode == 3:
            status = "is not </b>loaded</b>"
        elif result.returncode == 4:
            status = " reports a status of <b>dead</b>"
        else:
            status = "is in an <b>unknown state</b>"
        TEXT += f"<b>{service_name}</b>: is act {status}\n"

    await message.answer(TEXT, parse_mode='HTML')


async def show_logs(message: Message):
    service_name = message.text
    cmd = ['journalctl', '--unit', f'{service_name}.service', '-n', '25']  # Last 25 lines of logs for the service
    result = await asyncio.to_thread(subprocess.run, cmd, capture_output=True, text=True)
    if result.stdout:
        await message.answer(f"Logs for {service_name}:\n\n{result.stdout}")
    else:
        await message.answer(f"No logs found for {service_name} or an error occurred.")


async def service_logs(message: types.Message):
    await message.answer("Choose an option:", reply_markup=service_keyboard)


def register_system_info(dp: Dispatcher):
    dp.register_message_handler(get_system_info, commands=["system_info"], state="*")
    dp.register_message_handler(check_service, commands=["check_service"], state="*")
    dp.register_message_handler(service_logs, commands=["service_logs"], state="*")
    dp.register_message_handler(show_logs,
                                lambda message: message.text in [
                                                                 'order',
                                                                 'telegram bot',
                                                                 'image',
                                                                 'celery',
                                                                 'redis'],
                                state="*")
