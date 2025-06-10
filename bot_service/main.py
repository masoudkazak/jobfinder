from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from decouple import config
from fastapi import FastAPI

from .handlers.filters import filter_router

bot = Bot(token=config("BOTFATHER_API_TOKEN"))
dp = Dispatcher()
dp.include_router(filter_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Setting bot commands...")
    await bot.set_my_commands(
        [
            BotCommand(command="filter", description="فیلتر فرصت های شغلی"),
            BotCommand(command="search", description="جستجوی فرصت های شغلی"),
        ]
    )

    print("✅ Starting Telegram Bot polling...")
    await dp.start_polling(bot)
    yield
    print("🛑 Bot stopped.")


app = FastAPI(lifespan=lifespan)
