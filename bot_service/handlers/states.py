from aiogram.fsm.state import State, StatesGroup


class FilterStates(StatesGroup):
    filling_filters = State()
    typing_title = State()
