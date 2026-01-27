import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

def get_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏱ 5s", callback_data="t_5"),
         InlineKeyboardButton("⏱ 8s", callback_data="t_8"),
         InlineKeyboardButton("⏱ 15s", callback_data="t_15")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💎 **SYSTEM ANALITYCZNY V4.0**\nStrategia: `RSI Reversal` 📈\nPara: `EUR/USD OTC`",
        reply_markup=get_keyboard(),
        parse_mode="Markdown"
    )

async def handle_signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    sec = query.data.split("_")[1]
    msg = await query.message.reply_text("🔍 Sprawdzam wskaźnik RSI...")
    
    # SYMULACJA ANALIZY RSI
    await asyncio.sleep(1)
    rsi_value = random.randint(15, 85) # Bot "losuje" aktualne RSI
    
    if rsi_value > 70:
        direction = "PUT 🔴"
        reason = f"RSI Wysokie ({rsi_value}) - Rynek wykupiony"
    elif rsi_value < 30:
        direction = "CALL 🟢"
        reason = f"RSI Niskie ({rsi_value}) - Rynek wyprzedany"
    else:
        # Jeśli RSI jest w środku, bot szuka trendu
        direction = random.choice(["CALL 🟢", "PUT 🔴"])
        reason = "Momentum zgodne z trendem lokalnym"

    await msg.delete()
    await query.message.reply_text(
        f"🚨 **SYGNAŁ WYGENEROWANY**\n\n"
        f"📊 Para: `EUR/USD OTC`\n"
        f"📈 Kierunek: **{direction}**\n"
        f"🧠 Analiza: `{reason}`\n"
        f"⏱ Czas: `{sec}s`",
        parse_mode="Markdown",
        reply_markup=get_keyboard()
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_signal))
    app.run_polling(drop_pending_updates=True)
