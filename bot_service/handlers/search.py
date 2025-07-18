from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import httpx
from decouple import config
from ..formats import format_filters_human_readable, format_job

search_router = Router()


@search_router.message(Command("search"))
async def handle_search_command(message: Message):
    user_id = message.from_user.id
    user_filter = f"{config('DJANGO_API_URL')}/api/users/profile/{user_id}/"
    job_list_api = f"{config('DJANGO_API_URL')}/api/jobs/"
    
    async with httpx.AsyncClient() as client:
        try:
            response_profile = await client.get(user_filter)
            if response_profile.status_code == 404:
                await message.answer("موردی یافت نشد.")
                return
            user_data = response_profile.json()
            params = {
                "title": user_data["title"],
                "province": user_data["province"],
                "is_remote": user_data["remote_only"],
                "description": user_data["title"],
                "job_type": user_data["job_types"],
                "seniority_level": user_data["seniorities"],
                "min_salary": user_data["min_salary"],
                "max_salary": user_data["max_salary"],
                "salary_type": user_data["salary_type"],
                "skills": user_data["skills"],
            }
            response_jobs = await client.get(job_list_api, params=params)
            print(response_jobs.request.url)
            jobs_data = response_jobs.json()
            user_filter = format_filters_human_readable(user_data)

            await message.answer(user_filter)
            if not jobs_data:
                await message.answer("یافت نشد")
            for job_data in jobs_data:
                await message.answer(format_job(job_data))

        except Exception as e:
            print(f"{e}: ine")
            await message.answer(f"{e}: ine")
