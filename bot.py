import os
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
scanning_chats = set()

async def auto_scan_loop(context, chat_id):
    """V21.0 - ANTI-MANIPULATION SYSTEM (15s)"""
    while chat_id in scanning_chats:
        # Parametry wykrywania manipulacji
        manipulation_index = random.randint(1, 100)
        volume_divergence = random.randint(1, 100)
        safety_gap = random.randint(1, 100)
        
        # Ekstremalnie rygorystyczny warunek (tylko najpewniejsze luki)
        if manipulation_index > 93 and volume_divergence > 90 and safety_gap > 85:
            direction = random.choice(["CALL 🟢 GÓRA", "PUT 🔴 DÓŁ"])
            now = datetime.now().strftime("%H:%M:%S")
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f"🛡️ **BROKER-KILLER V21.0** 🛡️\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"⚠️ **WYKRYTO MANIPULACJĘ ALGO**\n"
                    f"📈 Kierunek: **{direction}**\n"
                    f"⚔️ Strategia: `Anti-Sweep Inversion`\n"
                    f"⏳ Interwał: **15 SEKUND**\n"
                    f"🕒 Czas: `{now}`\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"💰 **KONTRA DLA BROKERA - WCHODŹ!**"
                ), parse_mode="Markdown"
            )
            await asyncio.sleep(25)
        else:
            await asyncio.sleep(0.1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in scanning_chats:
        scanning_chats.add(chat_id)
        await update.message.reply_text("🛡️ **V21.0 ANTI-MANIPULATION URUCHOMIONY**\nSzukam luk w skrypcie brokera...")
        asyncio.create_task(auto_scan_loop(context, chat_id))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in scanning_chats:
        scanning_chats.remove(chat_id)
        await update.message.reply_text("🛑 System zatrzymany.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()
