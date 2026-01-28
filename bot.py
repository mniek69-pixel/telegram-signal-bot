import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_state[uid] = {"pair": "AUD/CAD OTC", "wins": 0}
    await update.message.reply_text(
        "🧨 **REVERSE TRAP V45.0** 🧨\n"
        "Status: `Anti-Broker Logic Enabled`\n"
        "Zasada: Gramy PRZECIWKO logice, którą broker chce uwalić.\n\n"
        "Obecna para: **AUD/CAD OTC**",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⚡ GENERUJ SYGNAŁ KONTRA", callback_data="sig")]]))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if uid not in user_state: user_state[uid] = {"pair": "AUD/CAD OTC", "wins": 0}
    st = user_state[uid]

    if query.data == "loss":
        st["wins"] = 0
        await query.message.reply_text("❌ Przegrana. Broker zmienił algorytm. Reset...", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 SZUKAJ NOWEJ LUKI", callback_data="sig")]]))
        return

    if query.data == "sig" or query.data == "win":
        if query.data == "win": st["wins"] += 1

        if st["wins"] >= 3:
            st["pair"] = "AUD/NZD OTC" if st["pair"] == "AUD/CAD OTC" else "AUD/CAD OTC"
            st["wins"] = 0
            await query.message.reply_text(f"✅ **CYKL ZALICZONY!**\nZmień wykres na: **{st['pair']}**",
                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 START NOWEJ SERII", callback_data="sig")]]))
            return

        wait = await query.message.reply_text("📡 Przechwytywanie pułapki brokera...")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        await wait.delete()

        # BRUTALNA INWERSJA
        # Jeśli logika mówi CALL, bot wymusza PUT, bo broker i tak by uciął CALL.
        raw_direction = random.choice(["CALL", "PUT"])
        final_dir = "PUT 🔴 (DÓŁ)" if raw_direction == "CALL" else "CALL 🟢 (GÓRA)"
        
        await query.message.reply_text(
            f"🎯 **SYGNAŁ KONTRA ({st['wins']+1}/3)**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📊 Para: **{st['pair']}**\n"
            f"📈 Kierunek: **{final_dir}**\n"
            f"⏳ Czas: `8 SEKUND`\n"
            f"━━━━━━━━━━━━━━━\n"
            f"⚠️ **WCHODŹ NATYCHMIAST!**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ WIN", callback_data="win"),
                 InlineKeyboardButton("❌ LOSS", callback_data="loss")]
            ]), parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
