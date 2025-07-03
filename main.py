#!/usr/bin/env python3
"""
YouTube Watchdog Bot
Telegram bot for YouTube playlist and subscription automation.
"""

import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)

logger = logging.getLogger(__name__)


async def setup_bot() -> tuple[Bot, Dispatcher]:
    """Initialize bot and dispatcher."""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        sys.exit(1)
    
    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    
    from bot.middlewares.access_control import AccessControlMiddleware
    from bot.middlewares.logging import SecureLoggingMiddleware
    
    dp.message.middleware(AccessControlMiddleware())
    dp.callback_query.middleware(AccessControlMiddleware())
    dp.message.middleware(SecureLoggingMiddleware())
    
    return bot, dp


async def setup_database():
    """Initialize database."""
    logger.info("Initializing database...")


async def setup_youtube_api():
    """Initialize YouTube API client."""
    youtube_client_id = os.getenv('YOUTUBE_CLIENT_ID')
    youtube_client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
    
    if not youtube_client_id or not youtube_client_secret:
        logger.error("YouTube API credentials not found in environment variables")
        sys.exit(1)
    
    logger.info("YouTube API credentials loaded")


async def setup_security():
    """Check security settings."""
    from utils.security import validate_secret_key, generate_secret_key
    from utils.access_control import is_access_restricted, get_allowed_users
    
    if not validate_secret_key():
        logger.error("SECRET_KEY not set or invalid")
        logger.info(f"Generated key example: {generate_secret_key()}")
        sys.exit(1)
    
    logger.info("SECRET_KEY is valid")
    
    if is_access_restricted():
        allowed_count = len(get_allowed_users())
        logger.info(f"Restricted access: {allowed_count} users allowed")
    else:
        logger.info("Open access for all users")


async def setup_scheduler():
    """Initialize task scheduler."""
    logger.info("Initializing task scheduler...")


async def setup_web_server():
    """Initialize web server for OAuth callbacks."""
    logger.info("Initializing web server for OAuth...")


async def main():
    """Main bot startup function."""
    logger.info("Starting YouTube Watchdog Bot...")
    
    try:
        await setup_security()
        await setup_database()
        await setup_youtube_api()
        await setup_scheduler()
        await setup_web_server()
        
        bot, dp = await setup_bot()
        
        start_router = Router()
        
        @start_router.message(Command("start"))
        async def start_handler(message: Message):
            await message.answer(
                "🎬 <b>YouTube Watchdog Bot</b>\n\n"
                "Hello! I'll help you automate YouTube tasks:\n"
                "• Playlist sorting (new videos to top)\n"
                "• New video monitoring from subscriptions\n"
                "• New content notifications\n\n"
                "<b>Available commands:</b>\n"
                "/login - YouTube authorization\n"
                "/sort_playlists - sort playlists\n"
                "/watch_channel - add channel for monitoring\n"
                "/settings - bot settings\n\n"
                "To get started, run /login"
            )
        
        dp.include_router(start_router)
        
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Bot started and ready to work")
        
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        sys.exit(1)
    finally:
        logger.info("Bot stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Received stop signal")
    except Exception as e:
        logger.error(f"Critical error: {e}")
        sys.exit(1) 