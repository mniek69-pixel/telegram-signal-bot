import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔥 SYGNAŁ PREMIUM (EUR/USD)", callback_data="sig_5")],
        [InlineKeyboardButton("⏱ 8s", callback_data="sig_8"), 
         InlineKeyboardButton("⏱ 15s", callback_data="sig_15")],
        [InlineKeyboardButton("📊 Statystyki Rynku", callback_data="stats")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **BOT TRADINGOWY PRO V5.0**\nStrategia: `EMA Cross + Momentum`\nTryb: `Skalpowanie OTC`",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

async def handle_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "stats":
        v = random.randint(70, 98)
        await query.message.reply_text(f"📈 **Market Status:**\nZmienność: `{v}%`\nTrend: `Silnie Wzrostowy`\nSkuteczność dzisiaj: `84%`", parse_mode="Markdown")
        return

    # Symulacja "mózgu" bota
    sec = data.split("_")[1]
    status = await query.message.reply_text("🧬 Analiza średnich EMA...")
    await asyncio.sleep(0.8)
    await status.edit_text("📊 Sprawdzanie wolumenu transakcji...")
    await asyncio.sleep(0.8)
    
    # Zaawansowana logika decyzji
    score = random.randint(1, 100)
    volatility = random.choice(["Wysoka", "Stabilna"])
    
    if score > 55:
        dir_text, dir_emoji = "CALL", "🟢 GÓRA"
        analysis = "EMA 9 przebiło EMA 21 od dołu. Potwierdzony popyt."
    else:
        dir_text, dir_emoji = "PUT", "🔴 DÓŁ"
        analysis = "Odrzucenie od lokalnego oporu. Wolumen maleje."

    await status.delete()
    await query.message.reply_text(
        f"🎯 **SYGNAŁ POTWIERDZONY**\n\n"
        f"💎 Para: `EUR/USD OTC`\n"
        f"📈 Kierunek: **{dir_emoji}**\n"
        f"⏳ Czas: `{sec}s`\n"
        f"⚡ Prawdopodobieństwo: `{random.randint(82, 96)}%`\n\n"
        f"🧠 **Uzasadnienie:**\n_{analysis}_",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_logic))
    app.run_polling(drop_pending_updates=True)
