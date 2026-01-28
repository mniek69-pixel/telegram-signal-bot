import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# Pamięć sesji (licznik kroków w sekwencji)
user_sessions = {}

def main_kb():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🎯 SZUKAJ SETUPU (AUD/CAD OTC)", callback_data="find_setup")
    ]])

def sequence_kb(step):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(f"✅ KROK {step} WYGRANY - DAWAJ DALEJ!", callback_data=f"step_{step+1}"),
        InlineKeyboardButton("❌ PRZEGRANA (RESET)", callback_data="find_setup")
    ]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🇦🇺 **AUD/CAD OTC - TRIPLE THREAT V41.0** 🇨🇦\n"
        "Tryb: `Kaskadowy (3 Wejścia)`\n"
        "Cel: Ominięcie manipulacji przez rozbicie pozycji.\n\n"
        "Kliknij, aby znaleźć główny impuls:",
        reply_markup=main_kb()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data
    await query.answer()

    if data == "find_setup":
        user_sessions[user_id] = {"step": 1, "dir": None}
        msg = await query.message.reply_text("📡 Skanowanie AUD/CAD OTC w poszukiwaniu luki...")
        await asyncio.sleep(1)
        
        # Losujemy kierunek raz dla całej serii 3 wejść (bo idziemy z prądem)
        direction = random.choice(["CALL 🟢 (GÓRA)", "PUT 🔴 (DÓŁ)"])
        user_sessions[user_id]["dir"] = direction
        
        await msg.delete()
        await query.message.reply_text(
            f"🔥 **WYKRYTO IMPULS! KROK 1/3** 🔥\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📊 Para: **AUD/CAD OTC**\n"
            f"📈 Kierunek: **{direction}**\n"
            f"⏳ Czas: `10-15s`\n"
            f"💪 Pewność: `⭐⭐⭐⭐⭐` (SMC Master)\n"
            f"━━━━━━━━━━━━━━━\n"
            f"⚡ **WEJDŹ TERAZ (1-szy strzał)!**",
            reply_markup=sequence_kb(1)
        )

    elif data.startswith("step_"):
        step = int(data.split("_")[1])
        
        if step > 3:
            await query.message.reply_text(
                "💰 **SEKWENCJA ZAKOŃCZONA!** 💰\n"
                "3/3 Wygrane. Broker nie zdążył zareagować.\n"
                "Zrób 2 minuty przerwy i zacznij nową serię.",
                reply_markup=main_kb()
            )
            return

        direction = user_sessions[user_id]["dir"]
        await query.message.reply_text(
            f"🚀 **KONTYNUACJA! KROK {step}/3** 🚀\n"
            f"Kierunek: **{direction}**\n"
            f"Wchodź natychmiast, póki pęd trwa!",
            reply_markup=sequence_kb(step)
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
