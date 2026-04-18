from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from gold_fetcher import get_gold_price
from ai_outlook import get_ai_outlook
from datetime import datetime
import re

# 🔑 YAHAN APNA BOT TOKEN DAALO
TOKEN = "8709546431:AAGmd7l9WzmQBnPVeoP73aZTjLhHt67H3Og"

def clean_outlook(text):
    """Remove ANSI escape sequences and control characters from Ollama output."""
    # ANSI escape codes pattern
    ansi_escape = re.compile(r'\x1b\[[0-9;]*[A-Za-z]|\x1b\[[0-9]*[KCD]')
    cleaned = ansi_escape.sub('', text)
    # Remove any remaining stray control characters
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', cleaned)
    # Remove extra spaces and normalize
    cleaned = ' '.join(cleaned.split())
    return cleaned

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏦 Skeletron Bullion AI\n\n"
        "Welcome to AI-powered gold intelligence.\n"
        "Commands:\n"
        "/gold - Get latest gold price & AI outlook\n"
        "/help - Show this message"
    )

async def gold_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Fetching latest gold data...")
    
    price, currency, timestamp = get_gold_price()
    if price:
        # Convert Unix timestamp to readable date-time
        try:
            dt = datetime.fromtimestamp(int(timestamp))
            readable_time = dt.strftime("%d %b %Y, %I:%M %p IST")
        except:
            readable_time = str(timestamp)
        
        outlook = get_ai_outlook(price)
        cleaned_outlook = clean_outlook(outlook)
        
        message = (
            f"*Gold Price (India)*\n"
            f"💰 ₹{price:,.2f} per ounce\n"
            f"📅 {readable_time}\n\n"
            f"*AI Market Outlook:*\n"
            f"{cleaned_outlook}\n\n"
            f"_Powered by Skeletron Bullion AI_"
        )
    else:
        message = "❌ Failed to fetch gold price. Please try later."
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n/gold - Gold price & AI outlook\n/start - Welcome message"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("gold", gold_command))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()