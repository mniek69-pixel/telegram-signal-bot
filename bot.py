import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
user_data = {}

def main_kb(step):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"✅ WIN ({step}/3)", callback_data=f"win_{step}"),
         InlineKeyboardButton("❌ LOSS", callback_data="loss")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"pair": "AUD/CAD OTC", "step": 1}
    await update.message.reply_text(
        "👻 **GHOST DELAY V44.0** 👻\n"
        "Status: `Invisibilty Mode Active`\n"
        "Para: **AUD/CAD OTC**\n\n"
        "Zasada: NIE KLIKAJ OD RAZU. Czekaj 2 sekundy po sygnale!",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 GENERUJ SYGNAŁ", callback_data="gen")]]))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data
    await query.answer()

    if user_id not in user_data: return
    state = user_data[user_id]

    if data == "loss":
        state["step"] = 1
        await query.message.reply_text("📉 Manipulacja wykryta. Resetuję profil...", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 SPRÓBUJ PONOWNIE", callback_data="gen")]]))
        return

    if data == "gen" or data.startswith("win_"):
        if data.startswith("win_"): state["step"] += 1

        if state["step"] > 3:
            state["pair"] = "AUD/NZD OTC" if state["pair"] == "AUD/CAD OTC" else "AUD/CAD OTC"
            state["step"] = 1
            await query.message.reply_text(f"🔄 **ZMIANA WYKRESU!** 🔄\nPrzejdź na: **{state['pair']}**",
                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 START NOWEJ SERII", callback_data="gen")]]))
            return

        # Generowanie sygnału z opóźnieniem "Ghost"
        loading = await query.message.reply_text("📡 Przechwytywanie danych OTC...")
        await asyncio.sleep(random.uniform(1.2, 2.5))
        await loading.delete()
        
        direction = random.choice(["CALL 🟢 (GÓRA)", "PUT 🔴 (DÓŁ)"])
        time_frame = random.choice(["8s", "10s"])
        
        await query.message.reply_text(
            f"👻 **SYGNAŁ GHOST ({state['step']}/3)**\n"
            f"━━━━━━━━━━━━━━━\n"
            f"💹 Para: **{state['pair']}**\n"
            f"📈 Kierunek: **{direction}**\n"
            f"⏳ Czas: `{time_frame}`\n"
            f"━━━━━━━━━━━━━━━\n"
            f"⚠️ **UWAGA:** Odlicz 2 sekundy w głowie i KLIKNIJ!",
            reply_markup=main_kb(state["step"]),
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
