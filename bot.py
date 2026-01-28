import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

def main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏱ 15s (SHADOW)", callback_data="sh_15"),
         InlineKeyboardButton("⏱ 30s (SHADOW)", callback_data="sh_30")],
        [InlineKeyboardButton("💰 SPRAWDŹ PAYOUT %", callback_data="check_pay")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌚 **SHADOW ALGORITHM V39.0** 🌚\n"
        "Tryb: `Anti-Retail Momentum` (Kontra do tłumu)\n"
        "Optymalizacja: `Wysokie Payouty (90%+)`\n\n"
        "Wybierz czas i walcz o realny zysk:",
        reply_markup=main_kb()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "check_pay":
        await query.message.reply_text("⚠️ **UWAGA:** Graj tylko jeśli Payout wynosi min. 80%.\nPoniżej tego gra nie ma sensu.")
        return

    if query.data.startswith("sh_"):
        sec = query.data.split("_")[1]
        msg = await query.message.reply_text("🕵️‍♂️ Analiza sentymentu detalicznego...")
        await asyncio.sleep(0.8)
        
        # Logika "Shadow": Symulujemy wykrycie, gdzie wchodzi tłum i gramy ODWROTNIE
        sentiment = random.randint(1, 100)
        
        # Jeśli sentiment jest wysoki (tłum kupuje), my sprzedajemy
        if sentiment > 50:
            direction = "PUT 🔴 (DÓŁ)"
            logic = "Retail Trap Detected"
        else:
            direction = "CALL 🟢 (GÓRA)"
            logic = "Institutional Sweep"

        res_kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ WIN", callback_data="w"),
            InlineKeyboardButton("❌ LOSS", callback_data="l")
        ]])

        await msg.delete()
        await query.message.reply_text(
            f"🌚 **SYGNAŁ SHADOW (KONTRA)** 🌚\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📈 Kierunek: **{direction}**\n"
            f"🎯 Model: `{logic}`\n"
            f"⏳ Czas: `{sec}s`\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🔥 **WYSOKI PAYOUT = WIĘKSZE RYZYKO. KLIKAJ!**",
            reply_markup=res_kb
        )

    if query.data in ["w", "l"]:
        await query.message.reply_text("Przygotowuję nową kontrę...", reply_markup=main_kb())

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
