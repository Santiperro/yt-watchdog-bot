"""Secure logging middleware."""

import logging
import re
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, Update


logger = logging.getLogger(__name__)


class SecureLoggingMiddleware(BaseMiddleware):
    """Middleware for secure event logging without sensitive data."""
    
    SENSITIVE_PATTERNS = [
        (r'token["\s]*[:=]["\s]*([a-zA-Z0-9._-]+)', r'token="***"'),
        (r'secret["\s]*[:=]["\s]*([a-zA-Z0-9._-]+)', r'secret="***"'),
        (r'password["\s]*[:=]["\s]*([a-zA-Z0-9._-]+)', r'password="***"'),
        (r'key["\s]*[:=]["\s]*([a-zA-Z0-9._-]+)', r'key="***"'),
        (r'(?:bearer|authorization)["\s]*[:=]["\s]*([a-zA-Z0-9._-]+)', r'authorization="***"'),
    ]
    
    def __init__(self, log_level: str = "INFO"):
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        logger.setLevel(self.log_level)
    
    def _sanitize_text(self, text: str) -> str:
        """Remove sensitive information from text."""
        if not text:
            return text
        
        sanitized = text
        for pattern, replacement in self.SENSITIVE_PATTERNS:
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    def _get_user_info(self, event: Message | CallbackQuery) -> str:
        """Get safe user information."""
        user = event.from_user
        if not user:
            return "unknown_user"
        
        user_info = f"user_id={user.id}"
        if user.username:
            user_info += f", username=@{user.username}"
        if user.first_name:
            user_info += f", name={user.first_name}"
        
        return user_info
    
    def _log_message(self, message: Message):
        """Log message safely."""
        user_info = self._get_user_info(message)
        chat_type = message.chat.type if message.chat else "unknown"
        
        text = self._sanitize_text(message.text or message.caption or "")
        if len(text) > 100:
            text = text[:97] + "..."
        
        logger.info(
            f"Message received: {user_info}, chat_type={chat_type}, "
            f"text='{text}', content_type={message.content_type}"
        )
    
    def _log_callback(self, callback: CallbackQuery):
        """Log callback query safely."""
        user_info = self._get_user_info(callback)
        data = self._sanitize_text(callback.data or "")
        
        logger.info(f"Callback received: {user_info}, data='{data}'")
    
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        """Log event and call next handler."""
        try:
            if hasattr(event, 'message') and event.message:
                self._log_message(event.message)
            elif hasattr(event, 'callback_query') and event.callback_query:
                self._log_callback(event.callback_query)
            
            result = await handler(event, data)
            return result
            
        except Exception as e:
            error_msg = self._sanitize_text(str(e))
            logger.error(f"Error in handler: {error_msg}")
            raise 