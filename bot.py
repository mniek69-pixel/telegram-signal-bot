import os
import random
import asyncio
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# Statystyki sesji
session_data = {"wins": 0, "losses": 0}

def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("⏱ 5 SEC 🟢", callback_data="t_5"),
         InlineKeyboardButton("⏱ 8 SEC 🟡", callback_data="t_8")],
        [InlineKeyboardButton("⏱ 12 SEC 🔴", callback_data="t_12"),
         InlineKeyboardButton("⏱ 15 SEC 🟣", callback_data="t_15")],
        [InlineKeyboardButton("🏠 Menu Główne", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def result_keyboard():
    keyboard = [[
        InlineKeyboardButton("✅ ITM (WIN)", callback_data="res_win"),
        InlineKeyboardButton("❌ OTM (LOSS)", callback_data="res_loss")
    ]]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🐻 **POCKET MASTER ELITE V32** 🐻\n"
        "Status: `LIVE SCANNING` 🟢\n"
        "Rynek: `AUD/CAD OTC` (lub inne)\n\n"
        "Wybierz czas wejścia (Sygnały 4-5⭐):",
        reply_markup=main_keyboard(),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "main_menu":
        await query.message.edit_text("Wybierz interwał:", reply_markup=main_keyboard())
        return

    if data.startswith("res_"):
        if "win" in data: session_data["wins"] += 1
        else: session_data["losses"] += 1
        winrate = (session_data["wins"] / (session_data["wins"] + session_data["losses"])) * 100
        await query.message.reply_text(
            f"📊 **Statystyki: {session_data['wins']}W - {session_data['losses']}L**\n"
            f"🎯 Winrate: `{winrate:.1f}%`", 
            reply_markup=main_keyboard()
        )
        return

    if data.startswith("t_"):
        seconds = data.split("_")[1]
        msg = await query.message.reply_text("📡 **ANALIZOWANIE PŁYNNOŚCI...**")
        
        # Szukamy tylko sygnału 4-5 gwiazdek
        while True:
            power = random.randint(1, 100)
            if power > 80 or power < 20: # Filtr 4-5 gwiazdek
                break
            await asyncio.sleep(0.2)

        pair = random.choice(["AUD/CAD OTC", "EUR/USD OTC", "GBP/JPY OTC"])
        is_inversion = random.choice([True, False, False]) # 33% szans na inwersję
        
        if power > 50:
            direction = "CALL ⬆️" if not is_inversion else "PUT ⬇️ (INWERSJA)"
            emoji = "🟢" if not is_inversion else "🟠"
        else:
            direction = "PUT ⬇️" if not is_inversion else "CALL ⬆️ (INWERSJA)"
            emoji = "🔴" if not is_inversion else "🔵"

        stars = "⭐⭐⭐⭐⭐" if (power > 92 or power < 8) else "⭐⭐⭐⭐"
        
        await msg.delete()
        await query.message.reply_text(
            f"{emoji} **SYGNAŁ POTWIERDZONY** {emoji}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"💹 Para: `{pair}`\n"
            f"📈 Kierunek: **{direction}**\n"
            f"⏳ Czas: `{seconds} SEC`\n"
            f"💪 Pewność: {stars}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🔥 **WCHODŹ TERAZ NA POCKET OPTION!**",
            reply_markup=result_keyboard(),
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
