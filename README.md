# CoinPulse Bot

📊 A Telegram bot for crypto market sentiment, trends, gas fees, and news.

## Features
- 📈 Real-time market sentiment
- 🔥 Trending topics tracking
- ⛽ Multi-chain gas fees
- 📰 Latest crypto news
- Interactive buttons and menus

## Deployment on Railway

1. Fork this repository to GitHub
2. Create a new project on Railway
3. Connect your GitHub repository
4. Add environment variables:
   - `TELEGRAM_BOT_TOKEN`: Your bot token from @BotFather
   - `WEBHOOK_URL`: Your Railway app URL (e.g., https://your-app.railway.app)
5. Deploy!

## Local Development

```bash
pip install -r requirements.txt
python bot.py
