import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

def time_keyboard():
    keyboard = [[
        InlineKeyboardButton("⏱ 5s", callback_data="time_5"),
        InlineKeyboardButton("⏱ 8s", callback_data="time_8"),
        InlineKeyboardButton("⏱ 15s", callback_data="time_15"),
    ]]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📡 Bot sygnałowy aktywny\nWybierz czas wejścia:",
        reply_markup=time_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    seconds = int(query.data.split("_")[1])

    await query.message.reply_text(f"⏳ Sygnał za {seconds} sekund...")
    await asyncio.sleep(seconds)

    signal = random.choice(["CALL 🟢", "PUT 🔴"])
    pair = "AUD/CAD OTC"

    await query.message.reply_text(
        f"🚨 SYGNAŁ!\nPara: {pair}\nKierunek: {signal}\nCzas: {seconds}s"
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

print("Bot działa...")
app.run_polling()
