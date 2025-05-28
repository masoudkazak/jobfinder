from aiogram import Router
from aiogram.types import Message
from decouple import config
import httpx

router = Router()


@router.message()
async def handle_message(message: Message):
    async with httpx.AsyncClient() as client:
        django_url = config("DJANGO_API_URL")
        response = await client.get(f"{django_url}/api/jobs/")
        jobs = response.json()

    text = "\n".join([f"🧑‍💻 {job['title']} @ {job['company']}" for job in jobs[:3]])
    await message.answer(text or "موردی یافت نشد.")
