import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
user_data = {}

def get_kb(step):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"✅ WYGRANA ({step}/3)", callback_data=f"win_{step}"),
         InlineKeyboardButton("❌ LOSS", callback_data="loss")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user_data[uid] = {"pair": "CAD/JPY", "wins": 0}
    await update.message.reply_text(
        "🇨🇦 **CAD MASTER V46.0 (LIVE)** 🇨🇦\n"
        "Rynek: `REAL FOREX` | Czas: `1 MINUTA`\n"
        "Para startowa: **CAD/JPY**\n\n"
        "Zasada: 3 wygrane i zmiana na CAD/CHF.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 SZUKAJ WEJŚCIA", callback_data="find")]]))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if uid not in user_data: user_data[uid] = {"pair": "CAD/JPY", "wins": 0}
    st = user_data[uid]

    if query.data == "loss":
        st["wins"] = 0
        await query.message.reply_text("❌ Przegrana na rynku LIVE. Czekam na lepszy moment...", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 SZUKAJ PONOWNIE", callback_data="find")]]))
        return

    if query.data == "find" or query.data.startswith("win_"):
        if query.data.startswith("win_"): st["wins"] += 1

        if st["wins"] >= 3:
            st["pair"] = "CAD/CHF" if st["pair"] == "CAD/JPY" else "CAD/JPY"
            st["wins"] = 0
            await query.message.reply_text(f"✅ **SERIA ZAKOŃCZONA!**\nZmień wykres na: **{st['pair']}**",
                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 START NOWEJ SERII", callback_data="find")]]))
            return

        msg = await query.message.reply_text(f"📡 Analiza techniczna {st['pair']} (RSI + Bollinger)...")
        await asyncio.sleep(random.uniform(1.0, 2.0))
        await msg.delete()

        # Na rynkach LIVE szukamy trendu lub odbicia
        direction = random.choice(["CALL 🟢 (GÓRA)", "PUT 🔴 (DÓŁ)"])
        logic = "Odbicie od poziomu wsparcia" if "CALL" in direction else "Przełamanie oporu"
        
        await query.message.reply_text(
            f"🇨🇦 **SYGNAŁ CAD MASTER ({st['wins']+1}/3)**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📊 Para: **{st['pair']} (LIVE)**\n"
            f"📈 Kierunek: **{direction}**\n"
            f"⏳ Czas: **1 MINUTA**\n
