# bot/keyboards/filters.py

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot_service.utils.constant import PROVINCES as provinces


def filter_menu_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="عنوان شغلی", callback_data="filter:title")
    keyboard.button(text="نوع همکاری", callback_data="filter:contract")
    keyboard.button(text="دورکاری", callback_data="filter:remote")
    keyboard.button(text="استان", callback_data="filter:province")
    keyboard.button(text="سطح تجربه", callback_data="filter:level")
    keyboard.button(text="ثبت", callback_data="filter:done")
    keyboard.adjust(2)
    return keyboard.as_markup()


def contract_type_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="تمام‌وقت", callback_data="contract:full")
    keyboard.button(text="پاره‌وقت", callback_data="contract:part")
    keyboard.button(text="پروژه‌ای", callback_data="contract:project")
    keyboard.button(text="کارآموزی", callback_data="contract:intern")
    keyboard.adjust(2)
    return keyboard.as_markup()


def remote_type_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✅ بله، فقط دورکاری", callback_data="remote:yes")
    keyboard.button(text="❌ نه، فرقی نمی‌کنه", callback_data="remote:no")
    keyboard.adjust(1)
    return keyboard.as_markup()


def level_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Junior", callback_data="level:junior")
    keyboard.button(text="Mid", callback_data="level:mid")
    keyboard.button(text="Senior", callback_data="level:senior")
    keyboard.adjust(3)
    return keyboard.as_markup()


def get_province_keyboard(page=0, per_page=5):
    start = page * per_page
    end = start + per_page
    current_page = provinces[start:end]

    keyboard = [
        [InlineKeyboardButton(text=prov, callback_data=f"province_select:{prov}")]
        for prov in current_page
    ]

    nav_buttons = []
    if start > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⬅️ قبلی", callback_data=f"province_page:{page - 1}"
            )
        )
    if end < len(provinces):
        nav_buttons.append(
            InlineKeyboardButton(
                text="➡️ بعدی", callback_data=f"province_page:{page + 1}"
            )
        )

    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
