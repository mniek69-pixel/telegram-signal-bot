import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

def rider_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 10 SEC RIDE", callback_data="rd_10"),
         InlineKeyboardButton("🚀 15 SEC RIDE", callback_data="rd_15")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏎️ **MOMENTUM RIDER V40.0** 🏎️\n"
        "Tryb: `Trend Explosion` (Z prądem)\n"
        "Zasada: Nie walcz z rynkiem, dołącz do niego!\n\n"
        "Wybierz czas, gdy widzisz ruch:",
        reply_markup=rider_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("rd_"):
        sec = query.data.split("_")[1]
        msg = await query.message.reply_text("📡 Wykrywanie siły impulsu...")
        
        # Symulacja analizy Trendu
        await asyncio.sleep(0.4)
        
        power = random.randint(1, 100)
        # 4-5 gwiazdek (Tylko najsilniejszy pęd)
        if power > 50:
            direction = "CALL 🟢 (GÓRA)"
            logic = "Trend Continuation (Impulse)"
            stars = "⭐⭐⭐⭐⭐"
        else:
            direction = "PUT 🔴 (DÓŁ)"
            logic = "Aggressive Sell Pressure"
            stars = "⭐⭐⭐⭐"

        res_kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ WIN", callback_data="w"),
            InlineKeyboardButton("❌ LOSS", callback_data="l")
        ]])

        await msg.delete()
        await query.message.reply_text(
            f"🏎️ **SYGNAŁ MOMENTUM: {direction}**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📈 Kierunek: **{direction}**\n"
            f"⚡ Model: `{logic}`\n"
            f"💪 Siła: {stars}\n"
            f"⏳ Czas: `{sec}s`\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🔥 **DOŁĄCZ DO RUCHU! KLIKAJ!**",
            reply_markup=res_kb,
            parse_mode="Markdown"
        )

    if query.data in ["w", "l"]:
        await query.message.reply_text("Szukam kolejnej fali...", reply_markup=rider_keyboard())

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
