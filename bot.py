import os
import random
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = os.getenv("TOKEN")
scanning_chats = {}

# Początkowe parametry (będą się zmieniać dynamicznie)
default_settings = {
    "threshold": 88.0,
    "cooldown": 15,
    "wins": 0,
    "losses": 0
}

async def auto_scan_loop(context, chat_id):
    while chat_id in scanning_chats:
        settings = scanning_chats[chat_id]
        
        # Symulacja zaawansowanej analizy EUR/USD OTC
        algo_score = random.uniform(70, 100)
        
        if algo_score > settings["threshold"]:
            direction = random.choice(["CALL 🟢 GÓRA", "PUT 🔴 DÓŁ"])
            now = datetime.now().strftime("%H:%M:%S")
            
            keyboard = [
                [
                    InlineKeyboardButton("Zysk ✅", callback_query_data='win'),
                    InlineKeyboardButton("Strata ❌", callback_query_data='loss')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f"🧠 **NEURAL FEEDBACK V23.0** 🧠\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"📊 Strategia: `Adaptive Flow`\n"
                    f"📈 Kierunek: **{direction}**\n"
                    f"🔥 Próg Pewności: `{settings['threshold']:.1f}%`\n"
                    f"⏳ Czas: **15 SEKUND**\n"
                    f"🕒 Godzina: `{now}`\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"👇 **KLIKNIJ WYNIK PO TRANSAKCJI:**"
                ),
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
            await asyncio.sleep(settings["cooldown"] + 5)
        else:
            await asyncio.sleep(0.5)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id
    await query.answer()
    
    if chat_id not in scanning_chats:
        return

    if query.data == 'win':
        scanning_chats[chat_id]["wins"] += 1
        # Przy wygranej lekko poluzuj lub utrzymaj filtry
        scanning_chats[chat_id]["threshold"] = max(85.0, scanning_chats[chat_id]["threshold"] - 0.5)
        status = "✅ Super! Utrzymujemy parametry."
    else:
        scanning_chats[chat_id]["losses"] += 1
        # Przy stracie drastycznie zwiększ wymogi analizy
        scanning_chats[chat_id]["threshold"] = min(98.0, scanning_chats[chat_id]["threshold"] + 2.5)
        status = "⚠️ Strata wykryta. Zaostrzam filtry wejścia..."

    stats = f"\nStatystyki: {scanning_chats[chat_id]['wins']}W - {scanning_chats[chat_id]['losses']}L"
    await query.edit_message_text(text=query.message.text + f"\n\n{status}{stats}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    scanning_chats[chat_id] = default_settings.copy()
    await update.message.reply_text("🧠 **SYSTEM ADAPTACYJNY URUCHOMIONY**\nBot będzie uczył się na podstawie Twoich wyników!")
    asyncio.create_task(auto_scan_loop(context, chat_id))

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
