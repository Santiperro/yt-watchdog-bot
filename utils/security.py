"""Security and data encryption utilities."""

import os
import base64
import logging
from typing import Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


logger = logging.getLogger(__name__)


class TokenEncryption:
    """Token encryption and decryption class."""
    
    def __init__(self):
        self._fernet = self._initialize_encryption()
    
    def _initialize_encryption(self) -> Optional[Fernet]:
        """Initialize Fernet with SECRET_KEY."""
        secret_key = os.getenv('SECRET_KEY')
        
        if not secret_key:
            logger.error("SECRET_KEY not found in environment variables")
            return None
        
        try:
            salt = b'yt_watchdog_salt'
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(secret_key.encode()))
            return Fernet(key)
        except Exception as e:
            logger.error(f"Failed to initialize encryption: {e}")
            return None
    
    def encrypt_token(self, token: str) -> Optional[str]:
        """Encrypt token."""
        if not self._fernet:
            logger.error("Encryption not initialized")
            return None
        
        try:
            encrypted_token = self._fernet.encrypt(token.encode())
            return base64.urlsafe_b64encode(encrypted_token).decode()
        except Exception as e:
            logger.error(f"Failed to encrypt token: {e}")
            return None
    
    def decrypt_token(self, encrypted_token: str) -> Optional[str]:
        """Decrypt token."""
        if not self._fernet:
            logger.error("Encryption not initialized")
            return None
        
        try:
            encrypted_data = base64.urlsafe_b64decode(encrypted_token.encode())
            decrypted_token = self._fernet.decrypt(encrypted_data)
            return decrypted_token.decode()
        except Exception as e:
            logger.error(f"Failed to decrypt token: {e}")
            return None
    
    def is_initialized(self) -> bool:
        """Check if encryption is initialized."""
        return self._fernet is not None


token_encryption = TokenEncryption()


def encrypt_user_token(token: str) -> Optional[str]:
    """Helper function to encrypt user token."""
    return token_encryption.encrypt_token(token)


def decrypt_user_token(encrypted_token: str) -> Optional[str]:
    """Helper function to decrypt user token."""
    return token_encryption.decrypt_token(encrypted_token)


def validate_secret_key() -> bool:
    """Validate SECRET_KEY correctness."""
    return token_encryption.is_initialized()


def generate_secret_key() -> str:
    """Generate new SECRET_KEY for initial setup."""
    return Fernet.generate_key().decode() 