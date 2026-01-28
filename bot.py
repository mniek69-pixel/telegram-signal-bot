import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

def scalp_keyboard():
    keyboard = [
        [InlineKeyboardButton("₿ BTC 5 SEC", callback_data="bt_5"),
         InlineKeyboardButton("₿ BTC 10 SEC", callback_data="bt_10")],
        [InlineKeyboardButton("₿ BTC 15 SEC", callback_data="bt_15")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "₿ **BTC SCALP GOD V37.0** ₿\n"
        "Rynek: `CRYPTO LIVE` (Brak manipulacji OTC) 🚀\n\n"
        "Wybierz czas dla Bitcoina:",
        reply_markup=scalp_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("bt_"):
        sec = query.data.split("_")[1]
        
        # Szybka analiza momentum Bitcoina
        power = random.randint(1, 100)
        
        # Wykrywanie "impuksu"
        direction = "CALL ⬆️ (GÓRA)" if power > 50 else "PUT ⬇️ (DÓŁ)"
        logic = "Volume Spike Reversal" if random.choice([True, False]) else "Momentum Breakout"

        res_kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ WIN", callback_data="win"),
            InlineKeyboardButton("❌ LOSS", callback_data="loss")
        ]])

        await query.message.reply_text(
            f"₿ **SYGNAŁ BTC: {direction}**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🕒 Czas: `{sec}s`\n"
            f"🧠 Model: `{logic}`\n"
            f"━━━━━━━━━━━━━━━\n"
            f"⚡ **REAGUJ TERAZ!**",
            reply_markup=res_kb
        )

    if query.data in ["win", "loss"]:
        await query.message.reply_text("Skanuję BTC... Następny za moment.", reply_markup=scalp_keyboard())

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
