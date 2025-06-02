from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from ..keyboards import filters
from .states import FilterStates

router = Router()


@router.message(Command("filter"))
async def start_filtering(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(FilterStates.filling_filters)
    await message.answer(
        "فیلتر های شغلی را وارد کنید.",
        reply_markup=filters.filter_menu_keyboard(),
    )


# Title
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
        "نوع همکاری را انتخاب کنید:",
        reply_markup=filters.contract_type_keyboard(with_done=True),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("contract:"))
async def select_contract(callback: types.CallbackQuery, state: FSMContext):
    value = callback.data.split(":")[1]
    data = await state.get_data()
    contract_list = data.get("contract", [])
    if value not in contract_list:
        contract_list.append(value)
        await state.update_data(contract=contract_list)
    await callback.answer("✅ اضافه شد")


@router.callback_query(F.data == "contract_done")
async def done_contract(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FilterStates.filling_filters)
    await callback.message.answer(
        "فیلتر بعدی رو انتخاب کن:", reply_markup=filters.filter_menu_keyboard()
    )
    await callback.answer()


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
    if value == "yes":
        value = True
    elif value == "no":
        value = False

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
        "سطح تجربه را انتخاب کنید:", reply_markup=filters.level_keyboard(with_done=True)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("level:"))
async def select_level(callback: types.CallbackQuery, state: FSMContext):
    value = callback.data.split(":")[1]
    data = await state.get_data()
    levels = data.get("level", [])
    if value not in levels:
        levels.append(value)
        await state.update_data(level=levels)
    await callback.answer("✅ اضافه شد")


@router.callback_query(F.data == "level_done")
async def done_level(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FilterStates.filling_filters)
    await callback.message.answer(
        "فیلتر بعدی رو انتخاب کن:", reply_markup=filters.filter_menu_keyboard()
    )
    await callback.answer()


# province
@router.callback_query(F.data == "filter:province")
async def show_provinces(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "استان موردنظر را انتخاب کنید:",
        reply_markup=filters.get_province_keyboard(with_done=True),
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
    data = await state.get_data()
    province_list = data.get("province", [])
    if province == "همه استان ها":
        province_list = [province]
    elif province not in province_list and "همه استان ها" not in province_list:
        province_list.append(province)
    await state.update_data(province=province_list)
    await callback.answer("✅ استان ذخیره شد")


@router.callback_query(F.data == "province_done")
async def done_province(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FilterStates.filling_filters)
    await callback.message.answer(
        "فیلتر بعدی رو انتخاب کن:", reply_markup=filters.filter_menu_keyboard()
    )
    await callback.answer()


# Skills
@router.callback_query(F.data == "filter:skills")
async def ask_for_skill(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "مهارت‌هات رو یکی یکی بنویس و بعد از هر مورد ارسال کن. وقتی تموم شد، روی دکمه زیر بزن:",
        reply_markup=filters.skill_done_keyboard(),
    )
    await state.set_state(FilterStates.typing_skill)
    await callback.answer()


@router.message(FilterStates.typing_skill)
async def collect_skills(message: types.Message, state: FSMContext):
    skill = message.text.strip()
    data = await state.get_data()
    skills = data.get("skills", [])
    if skill not in skills:
        skills.append(skill)
        await state.update_data(skills=skills)
        await message.answer(f"✅ '{skill}' ذخیره شد. ادامه بده یا روی 🔚 پایان بزن.")


@router.callback_query(F.data == "skills_done")
async def done_typing_skills(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    skills = data.get("skills", [])

    if not skills:
        await callback.answer("🚫 هیچ مهارتی وارد نکردی.")
        return

    await state.set_state(FilterStates.filling_filters)
    await callback.message.answer(
        "✅ مهارت‌ها ذخیره شدند.\nفیلتر بعدی رو انتخاب کن:",
        reply_markup=filters.filter_menu_keyboard(),
    )
    await callback.answer()


# Salary
@router.callback_query(F.data == "filter:salary")
async def ask_salary_type(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "نوع حقوق را انتخاب کنید:", reply_markup=filters.salary_type_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("salary:"))
async def handle_salary(callback: types.CallbackQuery, state: FSMContext):
    salary_type = callback.data.split(":")[1]
    if salary_type == "negotiable":
        await state.update_data(salary={"type": "negotiable"})
        await state.set_state(FilterStates.filling_filters)
        await callback.message.answer(
            "✅ حقوق توافقی ذخیره شد.", reply_markup=filters.filter_menu_keyboard()
        )
    else:
        await callback.message.edit_text("حداقل حقوق را به تومان وارد کن:")
        await state.set_state(FilterStates.typing_salary_min)
    await callback.answer()


@router.message(FilterStates.typing_salary_min)
async def get_salary_min(message: types.Message, state: FSMContext):
    try:
        salary_min = int(message.text)
        await state.update_data(salary={"type": "fixed", "min": salary_min})
        await state.set_state(FilterStates.typing_salary_max)
        await message.answer("حداکثر حقوق را وارد کن:")
    except ValueError:
        await message.answer("مقدار معتبر وارد کن (عدد تومان)")


@router.message(FilterStates.typing_salary_max)
async def get_salary_max(message: types.Message, state: FSMContext):
    try:
        salary_max = int(message.text)
        data = await state.get_data()
        salary = data.get("salary", {})
        salary["max"] = salary_max
        await state.update_data(salary=salary)
        await state.set_state(FilterStates.filling_filters)
        await message.answer(
            "✅ بازه حقوقی ذخیره شد.", reply_markup=filters.filter_menu_keyboard()
        )
    except ValueError:
        await message.answer("عدد معتبر وارد کن")


@router.callback_query(F.data == "filter:done")
async def finalize_filters(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = callback.from_user

    await save_user_filter_to_db(user_id, data)
    await state.clear()
    await callback.message.answer("✅ فیلترها با موفقیت ذخیره شدند.")
    await callback.answer()


async def save_user_filter_to_db(user_id: int, filters: dict):
    print(f"[DEBUG] Save to DB: user_id={user_id}, filters={filters}")
