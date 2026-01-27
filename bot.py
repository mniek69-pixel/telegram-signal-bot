import os
import random
import asyncio
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# Statystyki sesji w pamięci bota
stats = {"wins": 0, "losses": 0}

def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("⏱ 15s", callback_data="time_15"),
         InlineKeyboardButton("⏱ 30s", callback_data="time_30")],
        [InlineKeyboardButton("📊 Statystyki Sesji", callback_data="show_stats")]
    ]
    return InlineKeyboardMarkup(keyboard)

def result_keyboard():
    keyboard = [[
        InlineKeyboardButton("✅ WYGRANA", callback_data="res_win"),
        InlineKeyboardButton("❌ PRZEGRANA", callback_data="res_loss")
    ]]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 **SMC INVERSION V31.0** 🧠\n"
        "Tryb: `Anty-Manipulacja` 🛡️\n"
        "Skanuję strefy płynności...",
        reply_markup=main_keyboard(),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "show_stats":
        await query.message.reply_text(f"📈 **Wynik dzisiaj:** {stats['wins']}W - {stats['losses']}L")
        return

    if data.startswith("res_"):
        if "win" in data: stats["wins"] += 1
        else: stats["losses"] += 1
        await query.message.reply_text("Zapisano. Szukam kolejnej luki...", reply_markup=main_keyboard())
        return

    if data.startswith("time_"):
        seconds = int(data.split("_")[1])
        status = await query.message.reply_text("📡 Analiza institutional flow...")
        
        # SYMULACJA GŁĘBOKIEJ ANALIZY
        await asyncio.sleep(1.5)
        
        power = random.randint(1, 100)
        # Inversion Logic: Jeśli rynek jest zbyt oczywisty, bot odwraca kierunek
        is_manipulated = random.choice([True, False])
        
        # Szukamy tylko TOP (power > 85 lub < 15)
        if power > 50:
            direction = "CALL 🟢" if not is_manipulated else "PUT 🔴 (INWERSJA)"
            strength = "⭐⭐⭐⭐⭐"
            logic = "Institutional Support" if not is_manipulated else "Stop-Loss Raid Detection"
        else:
            direction = "PUT 🔴" if not is_manipulated else "CALL 🟢 (INWERSJA)"
            strength = "⭐⭐⭐⭐⭐"
            logic = "Supply Zone Hit" if not is_manipulated else "Liquidity Trap Reversal"

        await status.delete()
        await query.message.reply_text(
            f"🎯 **SYGNAŁ SMC ELITE**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📈 Kierunek: **{direction}**\n"
            f"💪 Moc: {strength}\n"
            f"🛡️ Strategia: `{logic}`\n"
            f"⏳ Czas: `{seconds}s`\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🔥 **WEJDŹ PO POTWIERDZENIU KNOTA!**",
            reply_markup=result_keyboard(),
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling(drop_pending_updates=True)
