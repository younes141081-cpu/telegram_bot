# Telegram Market Price Bot

A Telegram bot built with Python that provides market prices for selected assets using the Nobitex API.

Users can select an asset from a custom keyboard and receive its latest available price in Iranian Tomans.

## Features

- **Tether (USDT):** Retrieve the latest available market price.
- **Bitcoin (BTC):** Retrieve the latest available market price.
- **18-Karat Gold:** Estimate the price per gram based on the selected gold-linked market data.
- **Silver:** Estimate the price per gram based on the selected silver-linked market data.
- **Interactive Menu:** Navigate through the bot using Telegram reply keyboards.
- **Usage Rate Limiting:** Limit each user to 20 price requests per hour.
- **Error Handling:** Handle API and network errors without exposing technical details to users.
- **Price Conversion:** Convert prices from Iranian Rials to Tomans.

## Tech Stack

- Python
- python-telegram-bot
- Requests
- Nobitex API

## Project Structure

```text
telegram-market-price-bot/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

*The structure above is a suggested organization for the project.*

## Requirements

- Python 3.10 or newer
- A Telegram bot token
- Internet access
- Access to the Nobitex API

## Installation

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd telegram-market-price-bot
```

Replace `YOUR_REPOSITORY_URL` with your GitHub repository URL.

### 2. Install dependencies

```bash
pip install python-telegram-bot requests
```

### 3. Configure the bot token

Obtain a bot token from [@BotFather](https://t.me/BotFather).

Set the token as an environment variable instead of hardcoding it in the source code.

For PowerShell:

```powershell
$env:TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
```

The application must read this environment variable when initializing the Telegram bot.

### 4. Run the bot

```bash
python main.py
```

Open your bot in Telegram and send `/start`.

## Usage

1. Start the bot with `/start`.
2. Select **Choose Asset** from the main menu.
3. Choose Tether, Bitcoin, Gold, or Silver.
4. Receive the latest available price returned by the API.
5. Use the navigation buttons to return to the main menu.

## Rate Limiting

The bot allows each user to make up to 20 price requests within a rolling one-hour window.

The current implementation stores request timestamps in memory. Consequently, usage history is reset when the application restarts, and the limit is not shared across multiple application instances.

## Price Calculation

- Rial prices are converted to Tomans by dividing by 10.
- Gold and silver prices are estimated per gram using a troy ounce conversion factor of approximately 31.1034768 grams.
- The gold calculation applies a purity factor of 0.75 for 18-karat gold.

**Important:** Gold and silver estimates depend on the accuracy, units, and market definitions of the selected API symbols. They should be validated against the provider's current API documentation before being treated as actual spot prices.

## Error Handling

The bot handles API failures, network timeouts, unexpected responses, and missing market data by returning user-friendly error messages.

## Security

- Never commit Telegram bot tokens or other secrets to GitHub.
- Store credentials in environment variables.
- Keep `.env` out of version control.
- If a token is exposed, revoke it through BotFather and generate a replacement.

## Limitations

- Rate-limit data is stored in memory.
- Prices depend on the availability and accuracy of the external API.
- Market data may change between requests.
- Gold and silver calculations are estimates, not guaranteed market quotes.

## Future Improvements

- Persistent rate limiting using Redis or a database.
- Caching to reduce repeated API requests.
- Automated tests for price calculations and API failures.
- Structured logging.
- Configuration through environment variables.
- Improved input validation and API response handling.

## Disclaimer

This project is intended for educational and informational purposes. Prices may be delayed, unavailable, or inaccurate. This bot does not provide financial advice.

## License

No license has been specified yet.
