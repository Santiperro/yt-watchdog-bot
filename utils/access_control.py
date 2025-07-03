"""User access control utilities."""

import os
import logging
from typing import Set


logger = logging.getLogger(__name__)


def get_allowed_users() -> Set[int]:
    """Get list of allowed users from environment variables."""
    allowed_users_str = os.getenv('ALLOWED_USERS', '').strip()
    
    if not allowed_users_str:
        return set()
    
    try:
        user_ids = [
            int(user_id.strip()) 
            for user_id in allowed_users_str.split(',') 
            if user_id.strip()
        ]
        return set(user_ids)
    except ValueError as e:
        logger.error(f"Invalid ALLOWED_USERS format: {e}")
        return set()


def is_access_restricted() -> bool:
    """Check if restricted access mode is enabled."""
    return bool(get_allowed_users())


def is_user_allowed(user_id: int) -> bool:
    """Check if specific user has access."""
    allowed_users = get_allowed_users()
    
    if not allowed_users:
        return True
    
    return user_id in allowed_users


def log_access_attempt(user_id: int, username: str = None, allowed: bool = True):
    """Log access attempt."""
    user_info = f"user_id={user_id}"
    if username:
        user_info += f", username=@{username}"
    
    if allowed:
        logger.info(f"Access granted for {user_info}")
    else:
        logger.warning(f"Access denied for {user_info}") 