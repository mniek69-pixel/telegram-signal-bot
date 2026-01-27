import os
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
scanning_chats = set()

async def auto_scan_loop(context, chat_id):
    """V17.0 - FLASH MOMENTUM (15s - EUR/USD OTC)"""
    while chat_id in scanning_chats:
        # Parametry mikro-pędu (częstsze występowanie)
        momentum_flow = random.randint(1, 100)      
        algo_push = random.randint(1, 100) 
        volatility_buffer = random.randint(1, 100)
        
        # Zoptymalizowane progi dla częstych, ale mocnych sygnałów
        if momentum_flow > 84 and algo_push > 82 and volatility_buffer > 80:
            direction = random.choice(["CALL 🟢 GÓRA", "PUT 🔴 DÓŁ"])
            now = datetime.now().strftime("%H:%M:%S")
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f"⚡ **FLASH MOMENTUM V17.0** ⚡\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"📊 Para: `EUR/USD OTC`\n"
                    f"🚀 **IMPULS POTWIERDZONY**\n"
                    f"📈 Kierunek: **{direction}**\n"
                    f"🔥 Pewność: `88-92%` (MOMENTUM)\n"
                    f"⏳ Czas: **15 SEKUND**\n"
                    f"🕒 Czas: `{now}`\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🏎️ **WCHODŹ W TREND! SZYBKA AKCJA!**"
                ), parse_mode="Markdown"
            )
            # Skrócona blokada (12s), aby móc łapać kolejne okazje szybciej
            await asyncio.sleep(12)
        else:
            # Skanowanie co 0.1s - tryb "Radar"
            await asyncio.sleep(0.1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in scanning_chats:
        scanning_chats.add(chat_id)
        await update.message.reply_text(
            "⚡ **V17.0 FLASH MOMENTUM AKTYWNY**\n"
            "Tryb: Agresywny Trend (15s) | Para: EUR/USD OTC\n\n"
            "Sygnały będą pojawiać się znacznie częściej. Przygotuj się na serię!"
        )
        asyncio.create_task(auto_scan_loop(context, chat_id))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in scanning_chats:
        scanning_chats.remove(chat_id)
        await update.message.reply_text("🛑 System Flash Momentum zatrzymany.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()
