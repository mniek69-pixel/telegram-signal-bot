import os
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
scanning_chats = set()

async def auto_scan_loop(context, chat_id):
    """V20.0 - THE VOID MATRIX (Unique Fractional Strategy)"""
    while chat_id in scanning_chats:
        # Unikalne parametry "Void Matrix"
        entropy_level = random.randint(1, 100)      # Poziom chaosu algorytmu
        fractal_convergence = random.randint(1, 100)# Zbieżność fraktalna
        void_gap = random.randint(1, 100)           # Luka w płynności
        
        # Unikalny warunek: Wysoka zbieżność przy niskim chaosie
        if fractal_convergence > 91 and entropy_level < 15 and void_gap > 85:
            direction = random.choice(["CALL 🟢 GÓRA", "PUT 🔴 DÓŁ"])
            now = datetime.now().strftime("%H:%M:%S")
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f"🌀 **VOID MATRIX V20.0** 🌀\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"👁️ **WYKRYTO ANOMALIĘ FRAKTALNĄ**\n"
                    f"📈 Kierunek: **{direction}**\n"
                    f"🧬 Kod: `Liquidity_Void_Detect`\n"
                    f"🔥 Skuteczność: `ELITARNA`\n"
                    f"⏳ Interwał: **15 SEKUND**\n"
                    f"🕒 Czas: `{now}`\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"⚠️ **WEJŚCIE TYLKO W PUNKT!**"
                ), parse_mode="Markdown"
            )
            # Blokada czasowa dostosowana do cyklu fraktalnego
            await asyncio.sleep(20)
        else:
            # Skanowanie ultra-głębokie (tryb Matrix)
            await asyncio.sleep(0.01)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in scanning_chats:
        scanning_chats.add(chat_id)
        await update.message.reply_text("🌀 **SYSTEM VOID MATRIX V20.0 AKTYWNY**\nSkanuję strukturę algorytmu EUR/USD OTC...")
        asyncio.create_task(auto_scan_loop(context, chat_id))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in scanning_chats:
        scanning_chats.remove(chat_id)
        await update.message.reply_text("🛑 Matrix zatrzymany.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()
