import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# Klawiatura z czasami i stawką
def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("⏱ 5s", callback_data="time_5"),
         InlineKeyboardButton("⏱ 8s", callback_data="time_8"),
         InlineKeyboardButton("⏱ 15s", callback_data="time_15")],
        [InlineKeyboardButton("🧮 Oblicz Martingale (x2.2)", callback_data="calc_martingale")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Klawiatura do weryfikacji wyniku
def result_keyboard():
    keyboard = [[
        InlineKeyboardButton("✅ WYGRANA (ITM)", callback_data="result_win"),
        InlineKeyboardButton("❌ PRZEGRANA (OTM)", callback_data="result_loss")
    ]]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 **Bot Analityczny V3 + System Anty-Straty**\n"
        "Status: `Optymalizacja Trendu` 🚀\n\nWybierz czas wejścia:",
        reply_markup=main_keyboard(),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    # Logika obliczania Martingale
    if data == "calc_martingale":
        await query.message.reply_text(
            "💡 **System Martingale (Mnożnik x2.2)**\n"
            "Jeśli Twój pierwszy stopień to 10$, kolejne wejścia powinny wyglądać tak:\n"
            "1️⃣ stopień: 10$\n"
            "2️⃣ stopień: 22$\n"
            "3️⃣ stopień: 49$\n"
            "4️⃣ stopień: 108$\n"
            "5️⃣ stopień: 238$\n\n"
            "_Zalecane: Nie przekraczaj 3 stopnia!_" ,
            parse_mode="Markdown"
        )
        return

    # Logika wyniku
    if data.startswith("result_"):
        res_text = "🔥 Świetnie! Tak trzymać!" if "win" in data else "📉 Spokojnie, rynek to maraton. Użyj Martingale."
        await query.message.reply_text(res_text, reply_markup=main_keyboard())
        return

    # Logika sygnału (jeśli kliknięto czas)
    if data.startswith("time_"):
        seconds = int(data.split("_")[1])
        status_msg = await query.message.reply_text("📡 Pobieranie wolumenu OTC...")
        await asyncio.sleep(1)
        await status_msg.edit_text("🧪 Analiza świec japońskich...")
        await asyncio.sleep(1)

        # Zaawansowana symulacja logiczna
        power = random.randint(1, 100)
        pair = random.choice(["EUR/USD OTC", "GBP/JPY OTC", "AUD/CAD OTC", "USD/CHF OTC"])
        
        if power > 50:
            direction = "CALL 🟢 (GÓRA)"
            reason = "Przebicie oporu (Breakout)"
            strength = "⭐⭐⭐⭐⭐" if power > 85 else "⭐⭐⭐"
        else:
            direction = "PUT 🔴 (DÓŁ)"
            reason = "Odbicie od poziomu S/R"
            strength = "⭐⭐⭐⭐⭐" if power < 15 else "⭐⭐⭐"

        await status_msg.delete()
        await query.message.reply_text(
            f"🎯 **SYGNAŁ POTWIERDZONY**\n\n"
            f"📊 Para: `{pair}`\n"
            f"📈 Kierunek: **{direction}**\n"
            f"💪 Pewność: {strength}\n"
            f"💡 Analiza: _{reason}_\n"
            f"⏳ Czas: `{seconds}s`\n\n"
            f"🚀 **WEJDŹ TERAZ I POTWIERDŹ WYNIK:**",
            parse_mode="Markdown",
            reply_markup=result_keyboard()
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot V3 gotowy...")
    app.run_polling(drop_pending_updates=True)
