from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from decouple import config
from fastapi import FastAPI

from .handlers import router

bot = Bot(token=config("BOTFATHER_API_TOKEN"))
dp = Dispatcher()
dp.include_router(router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Starting Telegram Bot polling...")
    await dp.start_polling(bot)
    yield
    print("🛑 Bot stopped.")


app = FastAPI(lifespan=lifespan)
