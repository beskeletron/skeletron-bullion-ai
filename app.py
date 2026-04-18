import os
import asyncio
import logging
from aiohttp import web
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

# ---------- Import teri existing functions ----------
from gold_fetcher import get_gold_price
from ai_outlook import get_ai_outlook

# ----------------------------------------------------

load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")
RENDER_APP_URL = os.environ.get("RENDER_APP_URL", "https://your-app.onrender.com")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------- Telegram Bot Handlers (Same as before) ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏦 *Skeletron Bullion AI*\n\n"
        "Welcome to AI-powered gold intelligence.\n"
        "Commands:\n"
        "/gold - Get latest gold price & AI outlook\n"
        "/help - Show this message",
        parse_mode='Markdown'
    )

async def gold_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Fetching latest gold data...")
    price, currency, timestamp = get_gold_price()
    if price:
        from datetime import datetime
        try:
            dt = datetime.fromtimestamp(int(timestamp))
            readable_time = dt.strftime("%d %b %Y, %I:%M %p IST")
        except:
            readable_time = str(timestamp)
        outlook = get_ai_outlook(price)
        # Clean outlook
        import re
        ansi_escape = re.compile(r'\x1b\[[0-9;]*[A-Za-z]|\x1b\[[0-9]*[KCD]')
        cleaned_outlook = ansi_escape.sub('', outlook)
        cleaned_outlook = ' '.join(cleaned_outlook.split())
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
    await update.message.reply_text("Commands:\n/gold - Gold price & AI outlook\n/start - Welcome message")

# ---------- Self-Ping to prevent sleep ----------
async def self_ping():
    await asyncio.sleep(30)  # Wait for server to start
    while True:
        try:
            url = f"{RENDER_APP_URL}/health"
            requests.get(url, timeout=5)
            logger.info("Self-ping sent")
        except Exception as e:
            logger.error(f"Self-ping failed: {e}")
        await asyncio.sleep(600)  # 10 minutes

# ---------- Webhook Setup ----------
async def setup_webhook(application):
    webhook_url = f"{RENDER_APP_URL}/telegram"
    await application.bot.set_webhook(url=webhook_url)
    logger.info(f"Webhook set to {webhook_url}")

# ---------- Health Check Endpoint ----------
async def health(request):
    return web.Response(text="OK")

# ---------- Telegram Webhook Endpoint ----------
async def telegram_webhook(request):
    update = await request.json()
    update_obj = Update.de_json(update, application.bot)
    await application.process_update(update_obj)
    return web.Response(text="OK")

# ---------- Main Application ----------
if __name__ == "__main__":
    # Create bot application
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("gold", gold_command))

    # Create aiohttp web app
    web_app = web.Application()
    web_app.router.add_get("/health", health)
    web_app.router.add_post("/telegram", telegram_webhook)

    # Startup tasks
    async def on_startup(app):
        await application.initialize()
        await setup_webhook(application)
        asyncio.create_task(self_ping())
        logger.info("Bot started with webhook and self-ping")

    async def on_shutdown(app):
        await application.bot.delete_webhook()
        await application.shutdown()

    web_app.on_startup.append(on_startup)
    web_app.on_shutdown.append(on_shutdown)

    # Run web server
    port = int(os.environ.get("PORT", 8080))
    web.run_app(web_app, host="0.0.0.0", port=port)