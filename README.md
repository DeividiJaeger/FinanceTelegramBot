# FinanceTelegramBot

## About

FinanceTelegramBot is a Telegram bot that helps manage your finances by integrating with Google Sheets. It allows you to track expenses, incomes, and get financial reports directly from your Telegram.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- A Telegram account
- Google Developers account
- Access to the specific Google Sheet template

### Installation

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/FinanceTelegramBot.git
    cd FinanceTelegramBot
    ```

2. Set up your credentials:
    - Create a bot on Telegram using [BotFather](https://t.me/botfather)
    - Get the API token for your bot
    - Create a `.env` file in the project root with:
      ```
      TELEGRAM_BOT_TOKEN=your_telegram_bot_token
      ```
## Important Configuration Step

After downloading your `credentials.json` file from Google Developers Console:

1. Open the file and locate the `client_email` field
2. This email address is your bot's service account identity
3. **Share your Google Sheet** with this email address, giving it **Editor** permissions
4. Without this step, the bot won't be able to access or modify your spreadsheet

Example of sharing:
1. Open your Google Sheet
2. Click the "Share" button in the top right
3. Enter the service account email (looks like `bot-name@project-id.iam.gserviceaccount.com`)
4. Set permission to "Editor"
5. Click "Send"

3. Google Sheets integration:
    - Go to [Google Developers Console](https://console.developers.google.com/)
    - Enable the Google Sheets API
    - Create credentials for a service account
    - Download the `credentials.json` file and place it in the project root

### Running the Bot

Start the bot using Docker Compose:

```
docker-compose up --build
```

This command will:
- Install all required dependencies
- Build the Docker container
- Start the bot service

## Important Note

**This bot is configured to work with a specific Google Sheet template that is only accessible to the author**. The sheet structure is designed for specific financial tracking purposes. Contact the repository owner if you need access to the template or instructions to modify the code for your own sheet structure.