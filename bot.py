import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
user_state = {}

def get_ui(step, pair):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"✅ WYGRANA ({step}/3)", callback_data=f"win_{step}"),
         InlineKeyboardButton("❌ LOSS", callback_data="fail")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_state[user_id] = {"pair": "AUD/CAD OTC", "step": 1}
    await update.message.reply_text(
        "🧠 **GLITCH HUNTER V43.0** 🧠\n"
        "Status: `Infiltracja Algorytmu` ⚡\n"
        "Para: **AUD/CAD OTC**\n\n"
        "Zasada: Graj PRZECIWKO gwałtownym ruchom.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 SZUKAJ ANOMALII", callback_data="hunt")]]))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data
    await query.answer()

    if user_id not in user_state: return

    state = user_state[user_id]

    if data == "fail":
        state["step"] = 1
        await query.message.reply_text("📉 Algorytm nas przeczytał. Resetujemy serię.", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 PONÓW", callback_data="hunt")]]))
        return

    if data == "hunt" or data.startswith("win_"):
        if data.startswith("win_"): state["step"] += 1

        if state["step"] > 3:
            state["pair"] = "AUD/NZD OTC" if state["pair"] == "AUD/CAD OTC" else "AUD/CAD OTC"
            state["step"] = 1
            await query.message.reply_text(f"💎 **SERIA DOMKNIĘTA!** 💎\nUciekamy na parę: **{state['pair']}**",
                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 START NOWEJ SERII", callback_data="hunt")]]))
            return

        # Generowanie sygnału "Anomalii"
        msg = await query.message.reply_text("📡 Czekam na błąd serwera...")
        await asyncio.sleep(random.uniform(0.3, 0.8))
        
        direction = random.choice(["PUT 🔴 (DÓŁ)", "CALL 🟢 (GÓRA)"])
        
        await msg.delete()
        await query.message.reply_text(
            f"🎯 **ANOMALIA WYKRYTA! ({state['step']}/3)**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"💹 Para: **{state['pair']}**\n"
            f"📈 Kierunek: **{direction}**\n"
            f"⏳ Czas: `8 SEKUND`\n"
            f"⚠️ **WEJDŹ 2 RAZY (Double Tap)!**\n"
            f"━━━━━━━━━━━━━━━",
            reply_markup=get_ui(state["step"], state["pair"]),
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
