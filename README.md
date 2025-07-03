# YouTube Watchdog Bot

A Telegram bot for YouTube automation - sort your playlists and monitor new videos from your favorite channels.

## ✨ Features

- **Playlist Sorting**: Automatically move new videos to the top of your playlists
- **Channel Monitoring**: Watch specific YouTube channels and get notified about new uploads
- **Subscription Tracking**: Monitor all your YouTube subscriptions for new content
- **Secure OAuth**: Safe YouTube API authentication with encrypted token storage
- **Flexible Notifications**: Configure where to receive notifications (private messages or group chats)
- **Access Control**: Restrict bot usage to specific users if needed

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Telegram Bot Token ([get one from @BotFather](https://t.me/botfather))
- YouTube API credentials ([Google Cloud Console](https://console.cloud.google.com/))

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd yt-watchdog-bot
```

2. Install dependencies:
```bash
poetry install
```

3. Configure environment:
```bash
cp env.example .env
# Edit .env with your credentials
```

4. Run the bot:
```bash
poetry run python main.py
```

## 🤖 Bot Commands

### Authentication
- `/start` - Welcome message and setup instructions
- `/login` - Connect your YouTube account

### Playlist Management
- `/sort_playlists` - Sort all playlists (move new videos to top)
- `/sort_playlists now` - Force immediate sorting

### Channel Monitoring
- `/watch_channel CHANNEL_ID` - Start monitoring a specific channel
- `/check_subs` - Check all subscriptions for new videos

### Settings
- `/settings` - Manage bot configuration
- `/settings interval N` - Set check interval (in minutes)
- `/settings notify_target` - Configure notification destination
- `/settings playlists` - Select which playlists to sort

## 🔧 Configuration

Required environment variables:

```env
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token

# YouTube API
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_client_secret

# Security
SECRET_KEY=your_secret_encryption_key

# Access Control (optional)
ALLOWED_USERS=123456789,987654321  # Telegram user IDs (leave empty for public access)
```

See `env.example` for complete configuration options.

## 🛡️ Security

- OAuth tokens are encrypted before database storage
- Sensitive data filtering in logs
- Optional user access restrictions
- Local data storage (no third-party sharing)

## 📋 Development Status

Currently in active development. See `project_milestones.md` for detailed progress tracking.

**Current Version**: v0.1.0 (Basic infrastructure complete)
**Next**: YouTube API integration and playlist sorting

## 🤝 Contributing
This project follows structured development with milestone tracking. Check the current phase in `project_milestones.md` before contributing.

## 📄 License

**THIS CODE IS STRICTLY PROPRIETARY AND BELONGS EXCLUSIVELY TO THE AUTHOR. TAKING IT IS FORBIDDEN!!!!!**
