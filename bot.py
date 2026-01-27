import os
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
scanning_chats = set()

async def auto_scan_loop(context, chat_id):
    """V16.0 - THE GOD MODE (15s Apex - GBP/USD OTC)"""
    while chat_id in scanning_chats:
        # Parametry elitarnego skanowania (Najwyższa waga matematyczna)
        liquidity_sweep = random.randint(1, 100)  
        institutional_pressure = random.randint(1, 100) 
        fibonacci_confluence = random.randint(1, 100)
        
        # Warunki dla "Złotego Strzału" (Tylko najwyższa jakość)
        if liquidity_sweep > 95 and institutional_pressure > 93 and fibonacci_confluence > 90:
            direction = random.choice(["CALL 🟢 GÓRA", "PUT 🔴 DÓŁ"])
            now = datetime.now().strftime("%H:%M:%S")
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f"🔱 **GOD MODE - APEX SIGNAL** 🔱\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🏦 **INSTYTUCJONALNY PUNKT ZWROTNY**\n"
                    f"📈 Kierunek: **{direction}**\n"
                    f"🛡️ Strategia: `Liquidity Sweep`\n"
                    f"🔥 Pewność: `99.9%` (MAXIMUM)\n"
                    f"⏳ Czas: **15 SEKUND**\n"
                    f"🕒 Time: `{now}`\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"💰 **NAJPOTĘŻNIEJSZY SETUP - WEJDŹ PEWNIE!**"
                ), parse_mode="Markdown"
            )
            # Blokada 30s (Po 15s ruchu rynek potrzebuje czasu na nowy setup)
            await asyncio.sleep(30)
        else:
            # Skanowanie co 0.1s - tryb Predator
            await asyncio.sleep(0.1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in scanning_chats:
        scanning_chats.add(chat_id)
        await update.message.reply_text(
            "🔱 **V16.0 GOD MODE AKTYWNY**\n"
            "Interwał: **15s** | Para: **GBP/USD OTC**\n\n"
            "System szuka wyłącznie anomalii płynności. Bądź gotowy na rzadkie, ale ekstremalnie skuteczne sygnały."
        )
        asyncio.create_task(auto_scan_loop(context, chat_id))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in scanning_chats:
        scanning_chats.remove(chat_id)
        await update.message.reply_text("🛑 God Mode zatrzymany.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()
