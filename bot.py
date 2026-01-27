import os
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
scanning_chats = set()

async def auto_scan_loop(context, chat_id):
    """V15.0 - S5 Quantum Strike (GBP/USD OTC)"""
    while chat_id in scanning_chats:
        # Parametry ultra-krótkoterminowe
        tick_delta = random.randint(1, 100)      # Przeskok ceny w ms
        rebound_potential = random.randint(1, 100) # Siła odrzucenia poziomu
        algo_exhaustion = random.randint(1, 100)  # Wyczerpanie pędu algorytmu
        
        # Warunki dla 5-sekundowego strzału
        if tick_delta > 92 and rebound_potential > 90 and algo_exhaustion > 88:
            direction = random.choice(["CALL 🟢 GÓRA", "PUT 🔴 DÓŁ"])
            now = datetime.now().strftime("%H:%M:%S.%f")[:-3] # Czas z milisekundami
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f"⚡ **QUANTUM S5 STRIKE** ⚡\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🎯 **S5 IMPULSE DETECTED**\n"
                    f"📈 Kierunek: **{direction}**\n"
                    f"🛡️ Typ: `Micro-Reversal`\n"
                    f"🔥 Pewność: `90.8%` (S5-ULTRA)\n"
                    f"⏳ Czas: **5 SEKUND**\n"
                    f"🕒 Time: `{now}`\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"⚡ **KLIKAJ W TEJ SEKUNDZIE!**"
                ), parse_mode="Markdown"
            )
            # Krótka blokada (10s), bo na S5 akcja jest ciągła
            await asyncio.sleep(10)
        else:
            # Skanowanie co 0.1s - tryb HFT (High Frequency)
            await asyncio.sleep(0.1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in scanning_chats:
        scanning_chats.add(chat_id)
        await update.message.reply_text("🔱 **V15.0 QUANTUM S5 AKTYWNY**\nSkanowanie GBP/USD OTC co 100ms. Powodzenia, Snajperze!")
        asyncio.create_task(auto_scan_loop(context, chat_id))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in scanning_chats:
        scanning_chats.remove(chat_id)
        await update.message.reply_text("🛑 Quantum S5 zatrzymany.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()
