from aiogram.fsm.state import State, StatesGroup


class FilterStates(StatesGroup):
    filling_filters = State()

    typing_title = State()

    choosing_contract = State()
    choosing_remote = State()
    choosing_province = State()
    choosing_level = State()

    typing_skill = State()
    choosing_skills = State()

    choosing_salary_type = State()
    typing_salary_min = State()
    typing_salary_max = State()
