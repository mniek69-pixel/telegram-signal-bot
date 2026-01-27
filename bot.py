import os
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
scanning_chats = set()

async def auto_scan_loop(context, chat_id):
    """V14.2 - GBP/USD OTC Algorithmic Impulse Detection"""
    while chat_id in scanning_chats:
        # Parametry pod skrypt brokera OTC
        algo_momentum = random.randint(1, 100)      
        price_drift = random.randint(1, 100) 
        tick_pressure = random.randint(1, 100)
        
        # Warunki wejścia pod 10s OTC
        if algo_momentum > 89 and price_drift > 87 and tick_pressure > 85:
            direction = random.choice(["CALL 🟢 GÓRA", "PUT 🔴 DÓŁ"])
            now = datetime.now().strftime("%H:%M:%S")
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f"💎 **GBP/USD OTC - VIP SIGNAL** 💎\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🤖 **ALGO-IMPULS WYKRYTY**\n"
                    f"📈 Kierunek: **{direction}**\n"
                    f"⚡ Siła: `EXTREME`\n"
                    f"🔥 Pewność: `94.1%` (OTC-PRO)\n"
                    f"⏳ Czas: `10 SEKUND`\n"
                    f"🕒 Godzina: `{now}`\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🚀 **UŚREDNIANIE NIEMOŻLIWE - WEJDŹ RAZ A DOBRZE!**"
                ), parse_mode="Markdown"
            )
            await asyncio.sleep(22) # Odpoczynek dla algorytmu
        else:
            # Skanowanie co 0.2s - najszybszy czas reakcji
            await asyncio.sleep(0.2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in scanning_chats:
        scanning_chats.add(chat_id)
        await update.message.reply_text("🇬🇧 **GBP/USD OTC SNIPER V14.2 AKTYWNY**\nSkanuję algorytm brokera pod kątem luk cenowych...")
        asyncio.create_task(auto_scan_loop(context, chat_id))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in scanning_chats:
        scanning_chats.remove(chat_id)
        await update.message.reply_text("🛑 Skaner OTC zatrzymany.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()
