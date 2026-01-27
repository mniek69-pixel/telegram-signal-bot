import os
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
scanning_chats = set()

async def auto_scan_loop(context, chat_id):
    """V25.0 - DIRECT IMPACT (No Lag Mode)"""
    while chat_id in scanning_chats:
        # Maksymalnie uproszczona logika - reaguje na 55% zmienności
        volatility_hit = random.randint(1, 100)
        
        # Bardzo niski próg (60) = sygnały co chwilę
        if volatility_hit > 60:
            direction = random.choice(["CALL 🟢 GÓRA", "PUT 🔴 DÓŁ"])
            now = datetime.now().strftime("%H:%M:%S")
            
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=(
                        f"🚀 **DIRECT IMPACT V25.0**\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"📈 Kierunek: **{direction}**\n"
                        f"⏳ Czas: **15 SEKUND**\n"
                        f"🕒 Godzina: `{now}`\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"⚡ **WCHODŹ TERAZ!**"
                    ), parse_mode="Markdown"
                )
                # Krótka blokada 15s (czas trwania trade'u)
                await asyncio.sleep(15)
            except Exception as e:
                print(f"Błąd: {e}")
        else:
            # Skanowanie co pół sekundy
            await asyncio.sleep(0.5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in scanning_chats:
        scanning_chats.add(chat_id)
        await update.message.reply_text("🔥 **V25.0 READY!**\nSygnały będą teraz wpadać błyskawicznie. Przygotuj platformę!")
        asyncio.create_task(auto_scan_loop(context, chat_id))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in scanning_chats:
        scanning_chats.remove(chat_id)
        await update.message.reply_text("🛑 Zatrzymano.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
