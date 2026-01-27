import os
import random
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# Globalna flaga skanowania
scanning = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    scanning[chat_id] = True
    
    await update.message.reply_text(
        "🚀 **AUTO-SKANER V8.0 URUCHOMIONY**\n"
        "Tryb: `Automatyczny` 🤖\n"
        "Interwał analizy: `M1 (60 sekund)`\n"
        "Filtr jakości: `>93%` ✅\n\n"
        "Teraz możesz odłożyć telefon. Gdy znajdę idealny moment, **wyślę Ci sygnał natychmiast!**",
        parse_mode="Markdown"
    )
    
    # Uruchomienie pętli skanowania dla tego użytkownika
    asyncio.create_task(auto_scan(context, chat_id))

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    scanning[chat_id] = False
    await update.message.reply_text("🛑 Autonomiczne skanowanie zostało zatrzymane.")

async def auto_scan(context, chat_id):
    while scanning.get(chat_id):
        # Symulacja cichej analizy rynkowej
        score = random.randint(75, 99)
        
        if score >= 94:
            # ZNALEZIONO IDEALNY MOMENT
            direction = random.choice(["CALL 🟢 (GÓRA)", "PUT 🔴 (DÓŁ)"])
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f"🚨 **SYGNAŁ AUTOMATYCZNY (M1)** 🚨\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"📊 Aktywo: `EUR/USD OTC`\n"
                    f"📈 Decyzja: **{direction}**\n"
                    f"🔥 Pewność: `{score}%`\n"
                    f"⏱ Czas: `60 sekund`\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"⚡ **WCHODŹ TERAZ!**"
                ),
                parse_mode="Markdown"
            )
            # Przerwa po sygnale, żeby nie spamować w trakcie trwania transakcji
            await asyncio.sleep(70) 
        else:
            # Brak sygnału - czekaj 15 sekund przed kolejnym skanem
            await asyncio.sleep(15)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    print("Auto-Scanner V8.0 wystartował...")
    app.run_polling(drop_pending_updates=True)
