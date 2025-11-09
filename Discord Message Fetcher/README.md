# Discord Message Fetcher

A simple Python script to fetch messages from a Discord channel and save them to a text file. This tool runs locally and doesn't require server deployment.

## Features

- 📥 Fetch messages from any Discord channel you have access to
- 💾 Save messages to a text file with timestamps and author information
- 🔒 Secure token management using environment variables
- 📊 Support for fetching large numbers of messages (automatic pagination)
- 📎 Includes information about attachments and embeds
- 🔗 Extract all links from messages to a separate file
- 🚀 One-command setup and execution with `run.sh`

## Prerequisites

- Python 3.7 or higher
- A Discord account
- Access to the channel you want to fetch messages from

## Quick Start

### 1. Get Your Discord Token

**⚠️ IMPORTANT: Your Discord token is like a password. Never share it with anyone or commit it to GitHub!**

To get your Discord user token:

1. Open Discord in your web browser (not the desktop app)
2. Press `F12` to open Developer Tools
3. Go to the **Network** tab
4. Refresh the page (`F5` or `Ctrl+R`)
5. In the filter box, type `api`
6. Click on any request to `discord.com/api`
7. In the **Headers** section, scroll down to **Request Headers**
8. Find the `authorization` header - this is your token
9. Copy the token value (it usually starts with `mfa.` or is a long string)

**Alternative method (Desktop App):**
1. Open Discord Desktop App
2. Press `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Option+I` (Mac)
3. Go to the **Console** tab
4. Type: `(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()`
5. Press Enter - your token will be displayed
6. Copy the token (without quotes)

### 2. Get Your Channel ID

1. Enable Developer Mode in Discord:
   - Go to User Settings → Advanced → Enable "Developer Mode"
2. Right-click on the channel you want to fetch messages from
3. Click "Copy Channel ID"

### 3. Configure Environment Variables

The first time you run `run.sh`, it will automatically create a `.env` file from `.env.example`. Then you need to edit it:

1. Open the `.env` file in a text editor
2. Replace the placeholder values:
   ```
   DISCORD_TOKEN=your_actual_discord_token_here
   CHANNEL_ID=your_actual_channel_id_here
   ```

**⚠️ SECURITY NOTE:** The `.env` file is already in `.gitignore` to prevent accidentally committing your credentials to GitHub.

### 4. Run the Script

Simply execute the `run.sh` script. It will automatically:
- Create a virtual environment (if needed)
- Install all dependencies
- Run the message fetcher

**Basic usage (fetch 100 messages to messages.txt):**
```bash
./run.sh
```

**Fetch specific number of messages:**
```bash
./run.sh --limit 500
```

**Fetch ALL messages from the channel:**
```bash
./run.sh --limit all
```

**Specify output file:**
```bash
./run.sh --output my_messages.txt
```

**Combine options:**
```bash
./run.sh --limit 200 --output channel_backup.txt
```

**Fetch all messages to a custom file:**
```bash
./run.sh --limit all --output complete_backup.txt
```

**Extract all links from messages:**
```bash
./run.sh --extract-links
```

**Fetch all messages and extract links:**
```bash
./run.sh --limit all --extract-links
```

## Usage Examples

### Example 1: Default Usage
```bash
./run.sh
```
Output:
```
================================================================================
Discord Message Fetcher - Setup & Run
================================================================================
✓ Python 3 found: Python 3.10.0
✓ .env file found
✓ Virtual environment exists
✓ Dependencies installed

================================================================================
Starting Discord Message Fetcher...
================================================================================

================================================================================
Discord Message Fetcher
================================================================================

Channel ID: 123456789012345678
Messages to fetch: 100
Output file: messages.txt

Fetching messages from channel 123456789012345678...
Fetched 100 messages so far...

Successfully saved 100 messages to messages.txt

Done!
```

### Example 2: Custom Options
```bash
./run.sh --limit 500 --output backup.txt
```

### Example 3: Fetch All Messages
```bash
./run.sh --limit all
```
Output:
```
================================================================================
Discord Message Fetcher
================================================================================

Channel ID: 123456789012345678
Messages to fetch: All available messages
Output file: messages.txt

Fetching messages from channel 123456789012345678...
Fetched 100 messages so far...
Fetched 200 messages so far...
Fetched 300 messages so far...
...

Successfully saved 1523 messages to messages.txt

Done!
```

### Example 4: Extract Links
```bash
./run.sh --extract-links
```
Output:
```
================================================================================
Discord Message Fetcher
================================================================================

Channel ID: 123456789012345678
Messages to fetch: 100
Output file: messages.txt

Fetching messages from channel 123456789012345678...
Fetched 100 messages so far...

Successfully saved 100 messages to messages.txt

Extracting links...
Successfully saved 45 links to links.txt

Done!
```

## Command Line Options

- `-l, --limit NUMBER|all` - Number of messages to fetch, or "all" to fetch all available messages (default: 100)
- `-o, --output FILENAME` - Output file name (default: messages.txt)
- `--extract-links` - Extract all links from messages and save to links.txt
- `-h, --help` - Show help message

### Examples:
- `./run.sh` - Fetch 100 messages
- `./run.sh --limit 500` - Fetch 500 messages
- `./run.sh --limit all` - Fetch ALL messages from the channel
- `./run.sh --limit all --output backup.txt` - Fetch all messages to backup.txt
- `./run.sh --extract-links` - Fetch 100 messages and extract all links to links.txt
- `./run.sh --limit all --extract-links` - Fetch all messages and extract all links

## Output Format

### Messages Output (messages.txt)

The output text file will contain:
- Export metadata (total messages, export date)
- Messages in chronological order with:
  - Timestamp (UTC)
  - Author username
  - Message content
  - Attachment URLs (if any)
  - Embed information (if any)

Example:
```
Discord Messages Export
Total messages: 50
Exported on: 2025-11-07 19:13:10
================================================================================

[2025-11-07 15:30:45 UTC] Username: Hello, world!

[2025-11-07 15:31:20 UTC] AnotherUser: Check out this image!
  Attachments:
    - image.png: https://cdn.discordapp.com/attachments/...
```

### Links Output (links.txt)

When using `--extract-links`, a separate file will be created containing:
- All unique URLs found in message content
- Attachment URLs
- Embed URLs (images, videos, thumbnails)

Example:
```
Extracted Links
Total links: 45
Exported on: 2025-11-07 20:26:00
================================================================================

https://example.com/article
https://cdn.discordapp.com/attachments/123/456/image.png
https://youtube.com/watch?v=abc123
https://github.com/user/repo
```

## Manual Setup (Alternative to run.sh)

If you prefer to set up manually or are on Windows:

### 1. Create Virtual Environment
```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment
**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Script
```bash
python main.py --limit 100 --output messages.txt
```

## Troubleshooting

### "Invalid Discord token" Error
- Your token may have expired or is incorrect
- Re-obtain your token following the steps above
- Make sure there are no extra spaces in your `.env` file

### "Access forbidden" Error
- You don't have permission to view the channel
- Make sure you're logged into the correct Discord account
- Verify you can see the channel in Discord

### "Channel not found" Error
- The channel ID is incorrect
- Make sure you copied the full channel ID
- Verify the channel still exists

### "DISCORD_TOKEN not found" or "CHANNEL_ID not found" Error
- Make sure you've created the `.env` file
- Verify both `DISCORD_TOKEN` and `CHANNEL_ID` are set in `.env`
- Check for typos in the variable names

### Permission Denied when Running run.sh
```bash
chmod +x run.sh
```

## Security Best Practices

✅ **DO:**
- Keep your `.env` file private
- Use a virtual environment
- Regularly update your dependencies

❌ **DON'T:**
- Commit your `.env` file to Git (it's already in `.gitignore`)
- Share your Discord token with anyone
- Hardcode your token in the script

## Limitations

- Discord API rate limits apply (typically not an issue for personal use)
- Maximum 100 messages per API request (script handles pagination automatically)
- Only fetches text messages, attachments, and embeds (not voice/video)
- Requires user token (not a bot token)

## License

This project is provided as-is for personal use. Please respect Discord's Terms of Service when using this tool.

## Disclaimer

This tool is for personal use only. Using user tokens for automation may violate Discord's Terms of Service. Use at your own risk. The author is not responsible for any account actions taken by Discord.
