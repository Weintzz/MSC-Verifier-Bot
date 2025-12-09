# MSC-Verifier-Bot

MSC-Verifier-Bot is a Discord bot designed to verify members using a slash command `/verify`. It integrates with a SQL database to validate credentials and assigns roles accordingly.

## Features
- Slash command `/verify` for membership verification.
- Role assignment for verified and unverified members.
- Logging of verification events.
- Spam prevention in the verification channel.

## Prerequisites
- Python 3.8 or higher
- A Discord bot token
- A SQL database for storing verification data

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Weintzz/MSC-Verifier-Bot.git
   cd MSC-Verifier-Bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add the following variables:
   ```env
   BOT_TOKEN=your_discord_bot_token
   GUILD_ID=your_guild_id
   VERIFY_CHANNEL_ID=your_verify_channel_id
   LOGS_CHANNEL_ID=your_logs_channel_id
   VERIFIED_ROLE_ID=your_verified_role_id
   UNVERIFIED_ROLE_ID=your_unverified_role_id
   ```

## Usage

Run the bot using the following command:
```bash
python3 main.py
```

## Commands

### `/verify`
Verifies a member by checking their credentials against the SQL database.

Parameters:
- `msc_id`: Member's MSC ID
- `student_number`: Member's student number
- `email`: Member's email address

## Contributing

Feel free to submit issues or pull requests to improve the bot.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.