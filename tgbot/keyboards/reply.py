from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

service_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

button1 = KeyboardButton("order")
button2 = KeyboardButton("telegram bot")
button3 = KeyboardButton("image")
button4 = KeyboardButton("celery")
button5 = KeyboardButton("redis")

# Add buttons to the keyboard
service_keyboard.add(button1, button2)
service_keyboard.add(button3)
service_keyboard.add(button4, button5)
