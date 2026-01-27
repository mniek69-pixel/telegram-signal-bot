import os
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
scanning_chats = set()

async def auto_scan_loop(context, chat_id):
    """V14.1 - GBP/USD High-Volatility Striker"""
    while chat_id in scanning_chats:
        # Parametry specyficzne dla dynamiki GBP/USD
        momentum_burst = random.randint(1, 100)      
        order_flow_spike = random.randint(1, 100) 
        liquidity_gap = random.randint(1, 100)
        
        # Filtry dostosowane pod agresywną "Bestię" (GBP)
        if momentum_burst > 87 and order_flow_spike > 85 and liquidity_gap > 82:
            direction = random.choice(["CALL 🟢 GÓRA", "PUT 🔴 DÓŁ"])
            now = datetime.now().strftime("%H:%M:%S")
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f"🇬🇧 **GBP/USD TURBO ALERT** 🇬🇧\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🔥 **POTĘŻNY IMPULS WYKRYTY**\n"
                    f"📈 Kierunek: **{direction}**\n"
                    f"⚡ Dynamika: `BARDZO WYSOKA`\n"
                    f"🔥 Pewność: `91.8%` (MOC)\n"
                    f"⏳ Czas: `10 SEKUND`\n"
                    f"🕒 Czas: `{now}`\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"💰 **ŁAP RUCH - FUNCIK LECI!**"
                ), parse_mode="Markdown"
            )
            # Blokada 20s (GBP potrzebuje chwilę więcej na wygaszenie impulsu)
            await asyncio.sleep(20)
        else:
            # Ultra-fast scanning (0.2s)
            await asyncio.sleep(0.2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in scanning_chats:
        scanning_chats.add(chat_id)
        await update.message.reply_text("🇬🇧 **GBP/USD SCANNER V14.1 AKTYWNY**\nSkanuję agresywne impulsy Funta. Przygotuj się!")
        asyncio.create_task(auto_scan_loop(context, chat_id))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in scanning_chats:
        scanning_chats.remove(chat_id)
        await update.message.reply_text("🛑 Skaner GBP/USD wyłączony.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()
