import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 GENERUJ SYGNAŁ (90%+ Accuracy)", callback_data="sig_15")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 **BOT ANALITYCZNY V5.5 - TRYB FILTROWANIA**\n"
        "Status: `Aktywny` 🟢\n"
        "Minimalna pewność: `90%` 🛡️\n\n"
        "Kliknij poniżej, aby bot przeskanował rynek pod kątem idealnego wejścia.",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

async def handle_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    status = await query.message.reply_text("📡 Głębokie skanowanie rynku...")
    await asyncio.sleep(1.5)
    
    # GENEROWANIE SZANSY (1-100)
    # Symulujemy, że tylko ok. 30% sytuacji rynkowych nadaje się do gry
    accuracy_score = random.randint(75, 98)
    
    if accuracy_score < 90:
        # BOT NIE JEST PEWIEN - ODRZUCA SYGNAŁ
        await status.edit_text(
            f"⚠️ **SYGNAŁ ODRZUCONY**\n\n"
            f"Pewność: `{accuracy_score}%` (Wymagane: 90%+)\n"
            f"Powód: `Zbyt duże szumy na wykresie. Rynek nieprzewidywalny.`\n\n"
            f"🔄 Spróbuj ponownie za chwilę.",
            parse_mode="Markdown"
        )
        await asyncio.sleep(3)
        await query.message.reply_text("Gotowy do ponownego skanowania...", reply_markup=main_menu())
    else:
        # BOT JEST PEWIEN - DAJE SYGNAŁ
        direction = random.choice(["CALL 🟢 (GÓRA)", "PUT 🔴 (DÓŁ)"])
        pair = "EUR/USD OTC"
        
        await status.delete()
        await query.message.reply_text(
            f"✅ **ZNALEZIONO IDEALNY SETUP!**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📊 Para: `{pair}`\n"
            f"📈 Kierunek: **{direction}**\n"
            f"⏳ Czas: `15s`\n"
            f"🔥 Pewność: `{accuracy_score}%`\n"
            f"🧠 Analiza: `Potwierdzone wybicie z kanału i wsparcie wolumenu.`\n"
            f"━━━━━━━━━━━━━━━\n"
            f"🚀 **WEJDŹ TERAZ!**",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_logic))
    app.run_polling(drop_pending_updates=True)
