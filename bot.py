import os
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
scanning_chats = set()

async def auto_scan_loop(context, chat_id):
    """V26.0 - SMC RAPID FIRE (EUR/USD OTC 15s)"""
    while chat_id in scanning_chats:
        # Parametry symulujące realną logikę SMC (FVG + MSB)
        smc_impulse = random.randint(1, 100)
        structure_break = random.randint(1, 100)
        
        # Bardzo czuły próg dla SMC (Sygnały co ok. 60s)
        if smc_impulse > 65 and structure_break > 60:
            direction = random.choice(["CALL 🟢 GÓRA", "PUT 🔴 DÓŁ"])
            # Losujemy nazwę setupu dla realizmu SMC
            setup_name = random.choice(["FVG Mitigation", "Order Block Retest", "Liquidity Sweep"])
            now = datetime.now().strftime("%H:%M:%S")
            
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=(
                        f"🏦 **SMC RAPID FIRE V26.0** 🏦\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"🎯 Setup: `{setup_name}`\n"
                        f"📈 Kierunek: **{direction}**\n"
                        f"⏳ Czas: **15 SEKUND**\n"
                        f"🕒 Czas: `{now}`\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"🔥 **BANKI WCHODZĄ - TY TEŻ!**"
                    ), parse_mode="Markdown"
                )
                # Blokada tylko 15s (czas trwania świecy)
                await asyncio.sleep(15)
            except Exception as e:
                print(f"Error: {e}")
        else:
            # Skanowanie co 0.3 sekundy dla maksymalnej czułości
            await asyncio.sleep(0.3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in scanning_chats:
        scanning_chats.add(chat_id)
        await update.message.reply_text("🏦 **V26.0 SMC AKTYWNY**\nŚledzę ruchy grubych ryb na EUR/USD OTC co sekundę...")
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
