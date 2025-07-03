"""Access control middleware for bot."""

import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from utils.access_control import is_access_restricted, is_user_allowed, get_allowed_users, log_access_attempt


logger = logging.getLogger(__name__)


class AccessControlMiddleware(BaseMiddleware):
    """Middleware for checking user access to the bot."""
    
    def __init__(self):
        self.is_restricted = is_access_restricted()
        
        if self.is_restricted:
            allowed_count = len(get_allowed_users())
            logger.info(f"Access control enabled for {allowed_count} users")
        else:
            logger.info("Open access mode - bot available for all users")
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """Check user access."""
        user_id = event.from_user.id
        username = event.from_user.username
        
        if not self.is_restricted:
            log_access_attempt(user_id, username, allowed=True)
            return await handler(event, data)
        
        if not is_user_allowed(user_id):
            log_access_attempt(user_id, username, allowed=False)
            
            if isinstance(event, Message):
                await event.answer(
                    "🚫 <b>Access Denied</b>\n\n"
                    "This bot is available only for authorized users.\n"
                    "Contact administrator for access."
                )
            elif isinstance(event, CallbackQuery):
                await event.answer("Access denied", show_alert=True)
            
            return
        
        log_access_attempt(user_id, username, allowed=True)
        return await handler(event, data) 