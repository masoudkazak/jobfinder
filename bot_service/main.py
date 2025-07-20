from contextlib import asynccontextmanager
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from decouple import config
from fastapi import FastAPI

from .handlers.filters import filter_router
from .handlers.search import search_router
from .logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

bot = Bot(token=config("BOTFATHER_API_TOKEN"))

dp = Dispatcher()
dp.include_router(filter_router)
dp.include_router(search_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("✅ Setting bot commands...")
    await bot.set_my_commands(
        [
            BotCommand(command="filter", description="فیلتر فرصت های شغلی"),
            BotCommand(command="search", description="جستجوی فرصت های شغلی"),
        ]
    )

    logger.info("✅ Starting Telegram Bot polling...")
    await dp.start_polling(bot)
    yield
    logger.error("🛑 Bot stopped.")


app = FastAPI(lifespan=lifespan)
