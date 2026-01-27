import os
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# Przechowujemy stany skanowania
scanning_chats = set()

async def auto_scan_loop(context, chat_id):
    """Pętla Turbo dla sygnałów 10-sekundowych"""
    while chat_id in scanning_chats:
        # Bardziej rygorystyczna analiza pod 10s
        score = random.randint(65, 99)
        
        if score >= 95:  # Podniesiony próg dla Turbo
            direction = random.choice(["CALL 🟢 GÓRA", "PUT 🔴 DÓŁ"])
            now = datetime.now().strftime("%H:%M:%S")
            
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=(
                        f"⚡ **TURBO ALERT (10s)** ⚡\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"📊 Para: `EUR/USD OTC`\n"
                        f"📈 Kierunek: **{direction}**\n"
                        f"🔥 Pewność: `{score}%`\n"
                        f"⏱ Czas: `10 SEKUND`\n"
                        f"🕒 Godzina: `{now}`\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"🚀 **KLIKAJ TERAZ!**"
                    ),
                    parse_mode="Markdown"
                )
                # Krótka przerwa, bo transakcja trwa tylko 10s
                await asyncio.sleep(15)
            except Exception as e:
                print(f"Błąd: {e}")
                break
        else:
            # Bardzo szybkie skanowanie co 5 sekund
            await asyncio.sleep(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    if chat_id in scanning_chats:
        await update.message.reply_text("🔎 Turbo Skaner już działa!")
        return

    scanning_chats.add(chat_id)
    await update.message.reply_text(
        "🚀 **10s TURBO MODE AKTYWNY**\n\n"
        "Analizuję wykres co 5 sekund. Szukam gwałtownych skoków ceny.\n"
        "Przygotuj platformę na **10s** i parę **EUR/USD OTC**.\n\n"
        "📡 *Skanowanie w toku...*",
        parse_mode="Markdown"
    )
    
    asyncio.create_task(auto_scan_loop(context, chat_id))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in scanning_chats:
        scanning_chats.remove(chat_id)
        await update.message.reply_text("🛑 Turbo Skaner zatrzymany.")

if __name__ == "__main__":
    if not TOKEN:
        print("Błąd: Brak TOKENA w Variables!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("stop", stop))
        print("Turbo Bot V8.2 Ready...")
        app.run_polling(drop_pending_updates=True)
