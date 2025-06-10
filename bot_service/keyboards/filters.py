from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot_service.utils.constant import PROVINCES


def filter_menu_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="عنوان شغلی", callback_data="filter:title")
    keyboard.button(text="نوع همکاری", callback_data="filter:contract")
    keyboard.button(text="دورکاری", callback_data="filter:remote")
    keyboard.button(text="استان", callback_data="filter:province")
    keyboard.button(text="سطح تجربه", callback_data="filter:level")
    keyboard.button(text="مهارت‌ها", callback_data="filter:skills")
    keyboard.button(text="حقوق", callback_data="filter:salary")

    keyboard.button(text="✅ ثبت فیلترها", callback_data="filter:done")

    keyboard.adjust(2)
    return keyboard.as_markup()


def contract_type_keyboard(selected: list[str] | None = None, with_done: bool = True):
    selected = selected or []
    options = [
        ("تمام‌وقت", "full"),
        ("پاره‌وقت", "part"),
        ("پروژه‌ای", "project"),
        ("کارآموزی", "intern"),
    ]
    keyboard = InlineKeyboardBuilder()
    for label, key in options:
        check = "✅ " if key in selected else ""
        keyboard.button(text=check + label, callback_data=f"contract:{key}")
    if with_done:
        keyboard.button(text="🔚 پایان", callback_data="contract_done")
    keyboard.adjust(2)
    return keyboard.as_markup()


def remote_type_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✅ بله، فقط دورکاری", callback_data="remote:yes")
    keyboard.button(text="❌ نه، فرقی نمی‌کنه", callback_data="remote:no")
    keyboard.adjust(1)
    return keyboard.as_markup()


def level_keyboard(selected: list[str] | None = None, with_done: bool = True):
    selected = selected or []
    levels = [("Junior", "junior"), ("Mid", "mid"), ("Senior", "senior")]
    keyboard = InlineKeyboardBuilder()
    for label, key in levels:
        check = "✅ " if key in selected else ""
        keyboard.button(text=check + label, callback_data=f"level:{key}")
    if with_done:
        keyboard.button(text="🔚 پایان", callback_data="level_done")
    keyboard.adjust(3)
    return keyboard.as_markup()


def get_province_keyboard(
    selected: list[str] | None = None, page=0, per_page=6, with_done=True
):
    selected = selected or []
    start = page * per_page
    end = start + per_page
    current_page = PROVINCES[start:end]

    keyboard = [
        [
            InlineKeyboardButton(
                text=("✅ " if prov in selected else "") + prov,
                callback_data=f"province_select:{prov}",
            )
        ]
        for prov in current_page
    ]

    nav_buttons = []
    if start > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⬅️ قبلی", callback_data=f"province_page:{page - 1}"
            )
        )
    if end < len(PROVINCES):
        nav_buttons.append(
            InlineKeyboardButton(
                text="➡️ بعدی", callback_data=f"province_page:{page + 1}"
            )
        )
    if nav_buttons:
        keyboard.append(nav_buttons)
    if with_done:
        keyboard.append(
            [InlineKeyboardButton(text="🔚 پایان", callback_data="province_done")]
        )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def skill_done_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🔚 پایان", callback_data="skills_done")
    return keyboard.as_markup()


def salary_type_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="توافقی", callback_data="salary:negotiable")
    keyboard.button(text="ثابت", callback_data="salary:fixed")
    return keyboard.as_markup()
