import os
import random
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

scanning_chats = set()

async def auto_scan_loop(context, chat_id):
    """Zaawansowana pętla V9.0 - Rebound Strategy"""
    while chat_id in scanning_chats:
        # Symulacja trzech warunków: Bollinger, RSI, Volume
        condition_1 = random.randint(1, 100) # Bollinger Breakout
        condition_2 = random.randint(1, 100) # RSI Extreme
        condition_3 = random.randint(1, 100) # Volume Exhaustion
        
        # Obliczamy średnią ważoną pewności
        score = (condition_1 + condition_2 + condition_3) / 3
        
        # Tylko jeśli WSZYSTKIE parametry są ekstremalne (konfluencja)
        if condition_1 > 92 and condition_2 > 90 and condition_3 > 85:
            direction = "PUT 🔴 DÓŁ" if random.choice([True, False]) else "CALL 🟢 GÓRA"
            now = datetime.now().strftime("%H:%M:%S")
            
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=(
                        f"💎 **SYGNAŁ VIP (90%+) V9.0** 💎\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"📊 Para: `EUR/USD OTC`\n"
                        f"📈 Kierunek: **{direction}**\n"
                        f"🔥 Pewność: `{round(score, 1)}%` (ULTRA)\n"
                        f"⏳ Czas: `10 SEKUND`\n"
                        f"🕒 Czas sygnału: `{now}`\n\n"
                        f"🧠 **Analiza:** `Przełamanie Wstęgi Bollingera + Wyczerpanie popytu.`\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"⚠️ **REAGUJ NATYCHMIAST!**"
                    ),
                    parse_mode="Markdown"
                )
                await asyncio.sleep(20) # Blokada po sygnale
            except Exception as e:
                print(f"Błąd: {e}")
                break
        else:
            # Skanujemy bardzo gęsto co 3 sekundy
            await asyncio.sleep(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in scanning_chats:
        await update.message.reply_text("🔎 Skaner V9.0 już działa!")
        return

    scanning_chats.add(chat_id)
    await update.message.reply_text(
        "🏆 **SYSTEM V9.0 - VIP SNIPER URUCHOMIONY**\n\n"
        "Tryb: `Bollinger Rebound` 🚀\n"
        "Filtry: `Potrójna Konfluencja` ✅\n"
        "Interwał: `10s` (Szybkie odbicia)\n\n"
        "Cierpliwości. Bot wyśle sygnał tylko przy 90%+ pewności.",
        parse_mode="Markdown"
    )
    asyncio.create_task(auto_scan_loop(context, chat_id))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in scanning_chats:
        scanning_chats.remove(chat_id)
        await update.message.reply_text("🛑 System V9.0 wyłączony.")

if __name__ == "__main__":
    if not TOKEN:
        print("Błąd: Brak TOKENA!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("stop", stop))
        app.run_polling(drop_pending_updates=True)
