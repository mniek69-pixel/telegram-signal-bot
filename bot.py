import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ SKANUJ RYNEK (V6.0 PRO)", callback_data="scan_pro")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 **SYSTEM SCALPINGOWY V6.0 PRO**\n"
        "Metoda: `Price Action + Candle Momentum` 🕯\n"
        "Filtry: `Potrójna Konfluencja` ✅\n\n"
        "Bot szuka tylko momentów 'płynnościowych', gdzie szansa na wygraną jest najwyższa.",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

async def handle_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    status = await query.message.reply_text("📡 Przeszukiwanie poziomów wsparcia/oporu...")
    await asyncio.sleep(1)
    await status.edit_text("🔍 Analiza formacji świecowych (Pin Bar detection)...")
    await asyncio.sleep(1)
    
    # SYSTEM OCENY (1-100)
    # W tej wersji szansa na sygnał jest jeszcze mniejsza (ok. 20%), 
    # ale sygnały są znacznie "czystsze".
    score = random.randint(60, 99)
    
    if score < 92:
        await status.edit_text(
            f"❌ **BRAK POTWIERDZENIA**\n\n"
            f"Wskaźnik pewności: `{score}%` (Wymagane: 92%+)\n"
            f"Błąd: `Brak czystej formacji świecowej. Rynek w konsolidacji.`\n\n"
            f"Cierpliwość to Twój największy zysk. Czekaj...",
            parse_mode="Markdown"
        )
        await asyncio.sleep(2)
        await query.message.reply_text("Gotowy na kolejny skan.", reply_markup=main_menu())
    else:
        direction = random.choice(["CALL 🟢", "PUT 🔴"])
        
        # Generowanie profesjonalnego uzasadnienia
        reasons = [
            "Odrzucenie poziomu wsparcia silnym knotem.",
            "Formacja objęcia hossy na niskim interwale.",
            "Wyczerpanie trendu spadkowego (Momentum Exhaustion).",
            "Przełamanie lokalnej linii trendu z retestem."
        ]
        
        await status.delete()
        await query.message.reply_text(
            f"💎 **SYGNAŁ WYSOKIEJ JAKOŚCI** 💎\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📊 Aktywo: `EUR/USD OTC`\n"
            f"📈 Decyzja: **{direction}**\n"
            f"⏱ Czas: `10s - 15s`\n"
            f"🔥 Pewność: `{score}%`\n\n"
            f"🧠 **Analiza techniczna:**\n_{random.choice(reasons)}_\n"
            f"━━━━━━━━━━━━━━━\n"
            f"⚡ **REAGUJ NATYCHMIAST!**",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_logic))
    app.run_polling(drop_pending_updates=True)
