from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from ..keyboards import filters
from .states import FilterStates

router = Router()


@router.message(Command("filter"))
async def start_filtering(message: types.Message, state: FSMContext):
    await state.set_state(FilterStates.filling_filters)
    await message.answer(
        "لطفاً فیلترها را یکی‌یکی انتخاب کنید، و در پایان /done را ارسال کنید.",
        reply_markup=filters.filter_menu_keyboard(),
    )


# title
@router.callback_query(F.data == "filter:title")
async def title_value(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("عنوان شغلی را وارد کنید:")
    await state.set_state(FilterStates.typing_title)
    await callback.answer()


@router.message(FilterStates.typing_title)
async def receive_title(message: types.Message, state: FSMContext):
    title = message.text.strip()

    await state.update_data(title=title)
    await message.answer("✅ عنوان شغلی ذخیره شد:")

    await state.set_state(FilterStates.filling_filters)
    await message.answer(
        "فیلتر بعدی را انتخاب کن:", reply_markup=filters.filter_menu_keyboard()
    )


# Contract
@router.callback_query(F.data == "filter:contract")
async def contract_options(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "نوع همکاری را انتخاب کنید:", reply_markup=filters.contract_type_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("contract:"))
async def select_contract(callback: types.CallbackQuery, state: FSMContext):
    value = callback.data.split(":")[1]
    await state.update_data(contract=value)
    await callback.answer(
        "نوع همکاری ذخیره شد.", reply_markup=filters.contract_type_keyboard()
    )
    await state.set_state(FilterStates.filling_filters)
    await callback.message.answer(
        "فیلتر بعدی رو انتخاب کن:", reply_markup=filters.filter_menu_keyboard()
    )


# Remote
@router.callback_query(F.data == "filter:remote")
async def show_remote_options(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "دورکاری", reply_markup=filters.remote_type_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("remote:"))
async def select_remote(callback: types.CallbackQuery, state: FSMContext):
    value = callback.data.split(":")[1]
    await state.update_data(remote=value)
    await callback.answer(
        "وضعیت دورکاری ذخیره شد.", reply_markup=filters.remote_type_keyboard()
    )
    await callback.message.answer(
        "فیلتر بعدی رو انتخاب کن:", reply_markup=filters.filter_menu_keyboard()
    )


# level
@router.callback_query(F.data == "filter:level")
async def show_level_options(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "سطح تجربه:", reply_markup=filters.level_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("level:"))
async def select_level(callback: types.CallbackQuery, state: FSMContext):
    level = callback.data.split(":")[1]
    await state.update_data(level=level)
    await callback.answer("✅ سطح ذخیره شد.")
    await callback.message.answer(
        "فیلتر بعدی رو انتخاب کن:", reply_markup=filters.filter_menu_keyboard()
    )


# province
@router.callback_query(F.data == "filter:province")
async def show_provinces(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "استان موردنظر را انتخاب کنید:", reply_markup=filters.get_province_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("province_page:"))
async def change_province_page(callback: types.CallbackQuery):
    page = int(callback.data.split(":")[1])
    await callback.message.edit_text(
        "استان موردنظر را انتخاب کنید:",
        reply_markup=filters.get_province_keyboard(page=page),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("province_select:"))
async def select_province(callback: types.CallbackQuery, state: FSMContext):
    province = callback.data.split(":")[1]
    await state.update_data(province=province)
    await callback.answer(f"'{province}' انتخاب شد.")

    await state.set_state(FilterStates.filling_filters)
    await callback.message.answer(
        "فیلتر بعدی رو انتخاب کن:", reply_markup=filters.filter_menu_keyboard()
    )


@router.callback_query(F.data == "filter:done")
async def finalize_filters(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user.id

    await save_user_filter_to_db(user_id, data)
    await callback.message.answer("✅ فیلترها با موفقیت ذخیره شدند.")
    await state.clear()
    await callback.answer()


@router.message(Command("done"))
async def finish_filtering(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id

    await save_user_filter_to_db(user_id, data)

    await message.answer("✅ فیلترها با موفقیت ذخیره شدند.")
    await state.clear()


async def save_user_filter_to_db(user_id: int, filters: dict):
    print(f"[DEBUG] Save to DB: user_id={user_id}, filters={filters}")
