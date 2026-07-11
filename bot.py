import os
import logging
from datetime import datetime
from typing import Dict, List

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.constants import ParseMode

# ===== CONFIGURATION =====
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===== MOCK DATA =====
class CryptoData:
    @staticmethod
    def get_sentiment() -> Dict:
        return {
            "fear_greed": 52,
            "trend": "Sideways",
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M UTC")
        }
    
    @staticmethod
    def get_top_trends() -> List[Dict]:
        return [
            {"title": "Bitcoin ETF Flows", "sentiment": "Positive", "mentions": 1243},
            {"title": "Ethereum Layer 2 Growth", "sentiment": "Bullish", "mentions": 987},
            {"title": "Regulatory Updates EU", "sentiment": "Neutral", "mentions": 756},
            {"title": "DeFi TVL Recovery", "sentiment": "Bullish", "mentions": 634},
            {"title": "NFT Market Activity", "sentiment": "Bearish", "mentions": 512},
        ]
    
    @staticmethod
    def get_gas_fees() -> Dict:
        return {
            "ethereum": {"low": 8, "medium": 15, "high": 30},
            "polygon": {"low": 0.5, "medium": 1, "high": 2},
            "arbitrum": {"low": 0.3, "medium": 0.5, "high": 1},
        }
    
    @staticmethod
    def get_news() -> List[Dict]:
        return [
            {
                "title": "Major Bank Announces Crypto Custody Service",
                "source": "Financial Times",
                "time": "2 hours ago",
                "summary": "Leading financial institution expands into digital asset services."
            },
            {
                "title": "New Layer 2 Solution Launches Mainnet",
                "source": "CoinDesk",
                "time": "4 hours ago",
                "summary": "Scalability solution promises 100x throughput improvement."
            },
            {
                "title": "Regulatory Clarity in Asia Boosts Adoption",
                "source": "Reuters",
                "time": "6 hours ago",
                "summary": "New frameworks provide clearer guidelines for businesses."
            },
        ]

# ===== BOT HANDLERS =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when /start is issued."""
    user = update.effective_user
    welcome_message = f"""
📊 *Welcome to CoinPulse, {user.first_name}!*

Your crypto market intelligence bot. Get real-time sentiment, trends, gas fees, and news.

*Quick Commands:*
📈 /sentiment - Market sentiment
🔥 /trends - Top trends
⛽ /gas - Gas fees
📰 /news - Latest news
📊 /menu - All commands
❓ /help - Help

*Stay informed, stay prepared.*
"""
    
    keyboard = [
        [InlineKeyboardButton("📈 Sentiment", callback_data="sentiment"),
         InlineKeyboardButton("🔥 Trends", callback_data="trends")],
        [InlineKeyboardButton("⛽ Gas Fees", callback_data="gas"),
         InlineKeyboardButton("📰 News", callback_data="news")],
        [InlineKeyboardButton("📊 Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup,
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the main menu."""
    keyboard = [
        [InlineKeyboardButton("📈 Sentiment", callback_data="sentiment"),
         InlineKeyboardButton("🔥 Trends", callback_data="trends")],
        [InlineKeyboardButton("⛽ Gas Fees", callback_data="gas"),
         InlineKeyboardButton("📰 News", callback_data="news")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
         InlineKeyboardButton("❓ Help", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message = """
📊 *CoinPulse Main Menu*

Select an option below:
"""
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

async def sentiment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display current market sentiment."""
    data = CryptoData.get_sentiment()
    
    fear_greed = data['fear_greed']
    bar_length = 20
    filled = int((fear_greed / 100) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    if fear_greed < 30:
        emoji = "😱"
        level = "Extreme Fear"
    elif fear_greed < 45:
        emoji = "😰"
        level = "Fear"
    elif fear_greed < 55:
        emoji = "😐"
        level = "Neutral"
    elif fear_greed < 70:
        emoji = "😊"
        level = "Greed"
    else:
        emoji = "🚀"
        level = "Extreme Greed"
    
    message = f"""
📊 *Market Sentiment Update*

{emoji} *{level}* ({fear_greed}/100)

`{bar}`

*Trend:* {data['trend']}
*Updated:* {data['updated']}

💡 *Insight:* {level} suggests {'caution' if fear_greed < 45 else 'opportunity' if fear_greed > 55 else 'a balanced approach'}
"""
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data="sentiment"),
         InlineKeyboardButton("📊 Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

async def trends(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display top trending topics."""
    trends_data = CryptoData.get_top_trends()
    
    message = "🔥 *Top Trending Topics*\n\n"
    
    for i, trend in enumerate(trends_data, 1):
        sentiment_emoji = {
            "Bullish": "📈",
            "Bearish": "📉",
            "Positive": "✅",
            "Negative": "❌",
            "Neutral": "⚪",
        }.get(trend['sentiment'], "⚪")
        
        message += f"*{i}. {trend['title']}*\n"
        message += f"   {sentiment_emoji} {trend['sentiment']} • 💬 {trend['mentions']}\n\n"
    
    message += """
💡 *Tip:* High mentions = high interest. Use with other research.
"""
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data="trends"),
         InlineKeyboardButton("📊 Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

async def gas_fees(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display current gas fees."""
    gas_data = CryptoData.get_gas_fees()
    
    message = "⛽ *Current Gas Fees*\n\n"
    
    for chain, fees in gas_data.items():
        emoji = {
            "ethereum": "🔷",
            "polygon": "🟣",
            "arbitrum": "🔴",
        }.get(chain, "⚪")
        
        message += f"{emoji} *{chain.upper()}*\n"
        message += f"   🟢 Low: {fees['low']} Gwei\n"
        message += f"   🟡 Medium: {fees['medium']} Gwei\n"
        message += f"   🔴 High: {fees['high']} Gwei\n\n"
    
    message += """
💡 *Tip:* Wait for low fees to save on transactions.
"""
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data="gas"),
         InlineKeyboardButton("📊 Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display latest crypto news."""
    news_data = CryptoData.get_news()
    
    message = "📰 *Latest Crypto News*\n\n"
    
    for item in news_data:
        message += f"*{item['title']}*\n"
        message += f"📌 {item['source']} • {item['time']}\n"
        message += f"ℹ️ {item['summary']}\n\n"
    
    message += """
💡 *Tip:* Always verify information from multiple sources.
"""
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data="news"),
         InlineKeyboardButton("📊 Menu", callback_data="menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message."""
    help_text = """
❓ *CoinPulse Help*

*Available Commands:*
/start - Welcome message
/menu - Main menu
/sentiment - Market sentiment
/trends - Top trending topics
/gas - Gas fee estimates
/news - Latest news
/help - This message

*Features:*
• 📊 Market sentiment analysis
• 🔥 Trending topics
• ⛽ Multi-chain gas fees
• 📰 Crypto news

*Privacy:*
• No data stored
• Anonymous usage

*Support:* Coming soon!
"""
    
    keyboard = [[InlineKeyboardButton("📊 Menu", callback_data="menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show settings menu."""
    settings_text = """
⚙️ *Settings*

*Coming Soon:*
• 🔔 Daily updates
• 📈 Custom alerts
• 🌐 Language options
• 🎯 Personalized feed

*Currently in development.*
"""
    
    keyboard = [[InlineKeyboardButton("📊 Menu", callback_data="menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            settings_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
        await update.callback_query.answer()
    else:
        await update.message.reply_text(
            settings_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "sentiment":
        await sentiment(update, context)
    elif query.data == "trends":
        await trends(update, context)
    elif query.data == "gas":
        await gas_fees(update, context)
    elif query.data == "news":
        await news(update, context)
    elif query.data == "menu":
        await menu(update, context)
    elif query.data == "help":
        await help_command(update, context)
    elif query.data == "settings":
        await settings(update, context)
    else:
        await query.edit_message_text("Invalid option. Use /menu.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown messages."""
    await update.message.reply_text(
        "I'm not sure about that. Please use /menu to see available commands."
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ An error occurred. Please try again later or use /help."
        )

# ===== MAIN APPLICATION =====

def main() -> None:
    """Start the bot using polling mode."""
    if not TOKEN:
        logger.error("No TELEGRAM_BOT_TOKEN found!")
        return
    
    logger.info("Starting CoinPulse Bot in polling mode...")
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("sentiment", sentiment))
    application.add_handler(CommandHandler("trends", trends))
    application.add_handler(CommandHandler("gas", gas_fees))
    application.add_handler(CommandHandler("news", news))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("settings", settings))
    
    # Add button handler
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Add echo handler for unknown messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start polling
    logger.info("Bot is now running! Waiting for messages...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
