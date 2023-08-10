from aiogram.dispatcher.filters.state import State, StatesGroup


class UserAction(StatesGroup):
    username = State()
    date = State()
