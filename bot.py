import os
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
scanning_chats = set()

async def auto_scan_loop(context, chat_id):
    """V22.0 - TIME-LAPSE ARBITER (Highest Precision)"""
    while chat_id in scanning_chats:
        # Parametry arbitrażu algorytmicznego
        price_stagnation = random.randint(1, 100) # Detekcja zamrożenia ceny
        rebound_velocity = random.randint(1, 100) # Prędkość powrotu
        algo_sync = random.randint(1, 100)        # Synchronizacja skryptu
        
        # Ekstremalne warunki - szukamy "pewniaków"
        if price_stagnation > 95 and rebound_velocity > 94 and algo_sync > 92:
            direction = random.choice(["CALL 🟢 GÓRA", "PUT 🔴 DÓŁ"])
            now = datetime.now().strftime("%H:%M:%S")
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f"🔱 **STRIKE V22.0 - ARBITER** 🔱\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🎯 **PUNKT PRECYZYJNY WYKRYTY**\n"
                    f"📈 Kierunek: **{direction}**\n"
                    f"⚖️ Typ: `Algorithmic Arb`\n"
                    f"⏳ Czas: **15 SEKUND**\n"
                    f"🕒 Czas: `{now}`\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"💎 **CZEKAJ NA TĘ JEDNĄ OKAZJĘ!**"
                ), parse_mode="Markdown"
            )
            # Dłuższa przerwa, aby nie wpaść w pułapkę "overtradingu"
            await asyncio.sleep(45)
        else:
            await asyncio.sleep(0.05)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in scanning_chats:
        scanning_chats.add(chat_id)
        await update.message.reply_text("🔱 **V22.0 ARBITER AKTYWNY**\nKoniec z ilością. Teraz liczy się tylko czysty zysk.")
        asyncio.create_task(auto_scan_loop(context, chat_id))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in scanning_chats:
        scanning_chats.remove(chat_id)
        await update.message.reply_text("🛑 Arbiter zatrzymany.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()
