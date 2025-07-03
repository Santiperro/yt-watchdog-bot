# YouTube Watchdog Bot - Documentation

## Project Overview

YouTube Watchdog Bot is a Telegram bot for YouTube automation:
- Playlist sorting (new videos to the top)
- Monitoring new videos from subscriptions
- New content notifications
- OAuth2 authentication with YouTube API

## Architecture

### Main Components

```
yt-watchdog-bot/
├── main.py                     # Entry point
├── config/
│   ├── __init__.py
│   ├── settings.py             # Application settings
│   └── database.py             # Database configuration
├── bot/
│   ├── __init__.py
│   ├── handlers/               # Telegram handlers
│   │   ├── __init__.py
│   │   ├── auth.py            # /login commands
│   │   ├── playlists.py       # /sort_playlists
│   │   ├── monitoring.py      # /watch_channel, /check_subs
│   │   └── settings.py        # /settings commands
│   ├── middlewares/           # Bot middleware
│   │   ├── __init__.py
│   │   ├── access_control.py  # User access control
│   │   └── logging.py         # Secure logging
│   └── utils/                 # Bot utilities
├── youtube/
│   ├── __init__.py
│   ├── auth.py                # OAuth2 authentication
│   ├── client.py              # YouTube API client
│   ├── playlists.py           # Playlist operations
│   └── subscriptions.py       # Subscription monitoring
├── models/
│   ├── __init__.py
│   ├── user.py                # User model
│   ├── tokens.py              # Access tokens
│   ├── settings.py            # User settings
│   └── cache.py               # State cache
├── services/
│   ├── __init__.py
│   ├── scheduler.py           # Task scheduler
│   ├── notifications.py       # Notification system
│   └── playlist_sorter.py     # Sorting service
├── web/
│   ├── __init__.py
│   └── oauth_callback.py      # OAuth callback handler
└── utils/
    ├── __init__.py
    ├── logger.py              # Logging
    ├── security.py            # Token encryption/decryption
    ├── access_control.py      # User access verification
    └── helpers.py             # Common utilities
```

### Technology Stack

- **Bot Framework**: aiogram 3.x
- **YouTube API**: google-api-python-client
- **Database**: SQLite/PostgreSQL (SQLAlchemy ORM)
- **Scheduler**: APScheduler
- **Web Server**: aiohttp (for OAuth callbacks)
- **Environment**: python-dotenv

### Main Data Flows

#### 1. User Authentication
```
Telegram /login → OAuth URL → YouTube OAuth → Callback → Token Storage
```

#### 2. Playlist Sorting
```
/sort_playlists → Get Playlists → Find New Videos → Reorder → Notification
```

#### 3. Subscription Monitoring
```
Scheduler → Check Channels → Find New Videos → Compare with Cache → Notifications
```

## Modules

### bot/handlers/
Telegram bot command handlers:
- `auth.py` - OAuth authentication (/login)
- `playlists.py` - playlist management (/sort_playlists)
- `monitoring.py` - channel monitoring (/watch_channel, /check_subs)
- `settings.py` - settings (/settings)

### youtube/
YouTube API v3 integration:
- `auth.py` - OAuth2 flow, token refresh
- `client.py` - main API client
- `playlists.py` - playlist operations
- `subscriptions.py` - subscription handling and video search

### services/
Business logic:
- `scheduler.py` - background tasks (APScheduler)
- `notifications.py` - notification sending
- `playlist_sorter.py` - sorting algorithms

### models/
Data models (SQLAlchemy):
- `user.py` - Telegram users
- `tokens.py` - YouTube OAuth tokens
- `settings.py` - user settings
- `cache.py` - channel state cache

## User Commands

### Main Commands
- `/start` - welcome and instructions
- `/login` - YouTube authorization
- `/sort_playlists [now]` - sort playlists
- `/watch_channel CHANNEL_ID` - add channel for monitoring
- `/check_subs` - check for new videos
- `/settings` - manage settings

### Settings
- `/settings interval N` - check interval in minutes
- `/settings notify_target` - where to send notifications
- `/settings playlists` - select playlists for sorting

## Access Control

The bot supports two operation modes:

### Open Mode (default)
- `ALLOWED_USERS` variable is empty or not set
- Bot is accessible to all Telegram users

### Restricted Mode
- `ALLOWED_USERS` contains specific Telegram user_id values separated by commas
- Access only for specified users
- Unauthorized users receive access restriction message

Configuration example:
```env
# Access only for users with ID 123456789 and 987654321
ALLOWED_USERS=123456789,987654321

# Open access for everyone
ALLOWED_USERS=
```

## Data Security

### Security Principles
- **Token Encryption**: YouTube OAuth tokens are encrypted before saving to DB
- **Key Rotation**: Regular SECRET_KEY rotation for security
- **Minimal Permissions**: Bot requests only necessary scopes for YouTube API
- **Local Storage**: Database is stored locally, not shared with third parties

### Sensitive Data Storage
1. **YouTube Tokens**: Encrypted using SECRET_KEY before writing to DB
2. **User Settings**: Linked to Telegram user_id without additional identification
3. **Channel Cache**: Contains only public video information
4. **Logs**: Do not contain tokens or sensitive information

### Deployment Recommendations
- Use environment variables for all secrets
- Regularly update SECRET_KEY
- Restrict database file permissions (600)
- Use HTTPS for OAuth callbacks in production

## Environment Variables

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token

# YouTube API
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_client_secret
YOUTUBE_REDIRECT_URI=http://localhost:8080/oauth/callback

# Database
DATABASE_URL=sqlite:///./bot.db

# Web Server (for OAuth callbacks)
WEB_HOST=0.0.0.0
WEB_PORT=8080

# Access Control
ALLOWED_USERS=123456789,987654321  # Telegram user_id comma-separated (leave empty for all)

# Security
SECRET_KEY=your_secret_key_for_encryption  # For token encryption in DB

# Logging
LOG_LEVEL=INFO
```

## Installation and Running

### Development
```bash
poetry install
cp env.example .env  # and fill variables
poetry run python main.py
```

### Production
```bash
docker build -t yt-watchdog-bot .
docker run -d --env-file .env yt-watchdog-bot
```

## Change Log

### v0.1.0 (current)
- ✅ Created basic project structure
- ✅ Configured dependencies (aiogram, google-api-python-client, cryptography, etc.)
- ✅ Created task checklist in project_milestones.md
- ✅ Created project documentation
- ✅ Created main.py with basic bot initialization
- ✅ Configured environment variables template (env.example)
- ✅ Added /start command handler
- ✅ Added user access control system
- ✅ Designed data security architecture
- ✅ Added token encryption utilities
- ✅ Implemented middleware for access control and secure logging
- ✅ Created SECRET_KEY validation and security checks
- ✅ Created README.md with project overview and usage instructions

### Plans for Next Versions
- v0.2.0: Basic authentication and YouTube API
- v0.3.0: Playlist sorting
- v0.4.0: Subscription monitoring
- v0.5.0: Notification system
- v1.0.0: Full-featured release 