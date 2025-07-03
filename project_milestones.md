# YouTube Watchdog Bot - Milestones

## Main Development Stages

### 1. Basic Infrastructure
- [x] 1.1 Setup basic project structure
- [x] 1.2 Add dependencies (aiogram, google-api-python-client, etc.)
- [x] 1.3 Create main entry point main.py
- [x] 1.4 Setup environment variables (.env file)
- [x] 1.5 Basic Telegram bot handler
- [x] 1.6 Middleware for user access control
- [x] 1.7 Data encryption utilities (cryptography)
- [x] 1.8 Secure logging without sensitive data

### 2. YouTube API Integration
- [ ] 2.1 Setup OAuth2 authentication for YouTube API
- [ ] 2.2 Create YouTube API client
- [ ] 2.3 Implement access token retrieval
- [ ] 2.4 Save and refresh user tokens

### 3. User Authentication
- [ ] 3.1 /login command for OAuth2 authentication
- [ ] 3.2 Web interface for OAuth callback
- [ ] 3.3 Link Telegram user_id with YouTube tokens
- [ ] 3.4 Token validity verification

### 4. Playlist Sorting
- [ ] 4.1 /sort_playlists command
- [ ] 4.2 Get user's playlist list
- [ ] 4.3 Select playlists for sorting
- [ ] 4.4 Sorting algorithm (new videos to top)
- [ ] 4.5 Automatic sorting on schedule

### 5. Subscription Monitoring
- [ ] 5.1 /watch_channel command to add channels
- [ ] 5.2 Get user's subscription list
- [ ] 5.3 Search for new videos on tracked channels
- [ ] 5.4 State caching to identify new videos
- [ ] 5.5 /check_subs command for manual check

### 6. Notification System
- [ ] 6.1 Send notifications to private messages
- [ ] 6.2 /settings command for notification configuration
- [ ] 6.3 Support sending to group chats/channels
- [ ] 6.4 Notification format (link + title)

### 7. Settings and Configuration
- [ ] 7.1 /settings interval command for interval configuration
- [ ] 7.2 /settings notify_target command for chat selection
- [ ] 7.3 Save user settings to database
- [ ] 7.4 Commands for managing tracked channels

### 8. Task Scheduler
- [ ] 8.1 Background scheduler for periodic tasks
- [ ] 8.2 Automatic playlist sorting
- [ ] 8.3 Automatic new video checking
- [ ] 8.4 Execution interval management

### 9. Database
- [ ] 9.1 Data models (users, tokens, settings)
- [ ] 9.2 Database migrations
- [ ] 9.3 CRUD operations for all entities
- [ ] 9.4 Cache for tracking channel states

### 10. Data Security
- [ ] 10.1 Encrypt YouTube tokens before saving to DB
- [ ] 10.2 Secure SECRET_KEY storage in env variables
- [ ] 10.3 User input validation and sanitization
- [ ] 10.4 Restrict database file permissions
- [ ] 10.5 Logging without sensitive information

### 11. Finalization and Deployment
- [ ] 11.1 Docker containerization
- [ ] 11.2 Logging and monitoring
- [ ] 11.3 Error handling and retry logic
- [ ] 11.4 Deployment documentation 