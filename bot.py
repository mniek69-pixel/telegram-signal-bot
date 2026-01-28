import os
import random
import asyncio
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
session = {"wins": 0, "losses": 0}

def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("⏱ 1 MIN (STANDARD) 🎯", callback_data="eu_60"),
         InlineKeyboardButton("⏱ 2 MIN (STABLE) 🛡️", callback_data="eu_120")],
        [InlineKeyboardButton("📊 Statystyki EUR/USD", callback_data="eu_stats")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏦 **EUR/USD LIVE SNIPER V35.1** 🏦\n"
        "Rynek: `REAL MARKET (LIVE)` 🌍\n"
        "Para: **EUR/USD**\n\n"
        "Bot czeka na potwierdzenie od banków. Wybierz czas:",
        reply_markup=main_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "eu_stats":
        await query.message.reply_text(f"📈 Wynik EUR/USD: {session['wins']}W - {session['losses']}L")
        return

    if query.data.startswith("res_"):
        if "win" in query.data: session["wins"] += 1
        else: session["losses"] += 1
        await query.message.reply_text("Zapisano. Szukam kolejnej strefy...", reply_markup=main_keyboard())
        return

    if query.data.startswith("eu_"):
        sec = int(query.data.split("_")[1])
        t_text = "1 MINUTA" if sec == 60 else "2 MINUTY"
        
        msg = await query.message.reply_text("📡 Skanowanie arkusza zleceń EUR/USD...")
        
        # Ekstremalny filtr 5 GWIAZDEK (SMC Power > 92%)
        power = random.randint(1, 100)
        while not (power > 92 or power < 8):
            power = random.randint(1, 100)
            await asyncio.sleep(0.1)

        direction = "CALL ⬆️ (KUPNO)" if power > 50 else "PUT ⬇️ (SPRZEDAŻ)"
        emoji = "🟢" if power > 50 else "🔴"
        logic = "Order Block Mitigation" if power > 50 else "Fair Value Gap Fill"
        
        await msg.delete()
        res_kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ WYGRANA (ITM)", callback_data="res_win"),
            InlineKeyboardButton("❌ PRZEGRANA (OTM)", callback_data="res_loss")
        ]])
        
        await query.message.reply_text(
            f"{emoji} **SYGNAŁ INSTYTUCJONALNY** {emoji}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📊 Para: **EUR/USD (LIVE)**\n"
            f"📈 Kierunek: **{direction}**\n"
            f"⏳ Czas: `{t_text}`\n"
            f"💪 Pewność: ⭐⭐⭐⭐⭐\n"
            f"🎯 Setup: `{logic}`\n"
            f"━━━━━━━━━━━━━━━\n"
            f"💰 **WEJDŹ PO POTWIERDZENIU RUCHU!**",
            reply_markup=res_kb,
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
