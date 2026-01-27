import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Pobieranie tokena z Railway
TOKEN = os.getenv("TOKEN")

# Funkcja tworząca przyciski
def time_keyboard():
    keyboard = [[
        InlineKeyboardButton("⏱ 5s", callback_data="time_5"),
        InlineKeyboardButton("⏱ 8s", callback_data="time_8"),
        InlineKeyboardButton("⏱ 15s", callback_data="time_15"),
    ]]
    return InlineKeyboardMarkup(keyboard)

# Komenda /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Bot Sygnałowy gotowy!\nWybierz czas wejścia:",
        reply_markup=time_keyboard()
    )

# Obsługa kliknięć w przyciski
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    seconds = int(query.data.split("_")[1])
    await query.edit_message_text(f"⏳ Analiza rynku... Sygnał za {seconds}s")
    
    # Odliczanie
    await asyncio.sleep(seconds)

    # Losowy sygnał (później tu dodamy Twoją strategię)
    signal = random.choice(["CALL 🟢 (GÓRA)", "PUT 🔴 (DÓŁ)"])
    pair = random.choice(["EUR/USD OTC"])

    await query.message.reply_text(
        f"🚨 **NOWY SYGNAŁ** 🚨\n\n"
        f"📊 Para: **{pair}**\n"
        f"📈 Kierunek: **{signal}**\n"
        f"⏱ Czas: **{seconds}s**\n"
        f"🔥 Wejdź TERAZ!",
        parse_mode="Markdown"
    )
    # Ponowne wysłanie menu po sygnale
    await query.message.reply_text("Wybierz czas na kolejny sygnał:", reply_markup=time_keyboard())

# Uruchomienie bota
if __name__ == "__main__":
    if not TOKEN:
        print("BŁĄD: Nie znaleziono TOKENA w zmiennych Railway!")
    else:
        print("Bot startuje...")
        app = ApplicationBuilder().token(TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_handler))
        
        # Kluczowe: drop_pending_updates sprawia, że bot nie wariuje po restarcie
        app.run_polling(drop_pending_updates=True)
