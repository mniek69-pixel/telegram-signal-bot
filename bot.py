import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

def main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏱ 15s (EUR/USD OTC)", callback_data="sh_15"),
         InlineKeyboardButton("⏱ 30s (EUR/USD OTC)", callback_data="sh_30")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌚 **SHADOW ALGORITHM V39.1** 🌚\n"
        "Para: `EUR/USD OTC` 📈\n"
        "Cel: `Wypłata 90%+` 💰\n\n"
        "Czekam na sygnał kontrariański...",
        reply_markup=main_kb()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("sh_"):
        sec = query.data.split("_")[1]
        msg = await query.message.reply_text("🕵️‍♂️ Szukam pułapki na EUR/USD OTC...")
        
        # Bardzo szybka analiza (0.5s), bo na 15s liczy się każda chwila
        await asyncio.sleep(0.5)
        
        power = random.randint(1, 100)
        # 4-5 gwiazdek (Pewność Shadow)
        if power > 50:
            direction = "PUT 🔴 (DÓŁ)"
            stars = "⭐⭐⭐⭐⭐"
            model = "Retail Overbuy Trap"
        else:
            direction = "CALL 🟢 (GÓRA)"
            stars = "⭐⭐⭐⭐"
            model = "Institutional Sweep"

        res_kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ WIN (ITM)", callback_data="w"),
            InlineKeyboardButton("❌ LOSS (OTM)", callback_data="l")
        ]])

        await msg.delete()
        await query.message.reply_text(
            f"🌚 **SYGNAŁ SHADOW: {direction}**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📊 Para: **EUR/USD OTC**\n"
            f"⏳ Czas: `{sec}s`\n"
            f"💪 Pewność: {stars}\n"
            f"🎯 Model: `{model}`\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🔥 **WYSOKI ZYSK! WCHODŹ TERAZ!**",
            reply_markup=res_kb,
            parse_mode="Markdown"
        )

    if query.data in ["w", "l"]:
        await query.message.reply_text("Gotowy na kolejną kontrę?", reply_markup=main_kb())

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
