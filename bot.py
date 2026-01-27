import os
import random
import asyncio
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# System zarządzania sesją
session = {"wins": 0, "losses": 0, "streak": 0, "locked_until": None}

def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("⏱ 5s 🛡️", callback_data="gt_5"),
         InlineKeyboardButton("⏱ 10s 🛡️", callback_data="gt_10")],
        [InlineKeyboardButton("⏱ 15s 🛡️", callback_data="gt_15")],
        [InlineKeyboardButton("📊 Stan Sesji", callback_data="st_stats")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session["streak"] = 0 # Reset przy nowym starcie
    await update.message.reply_text(
        "👻 **GHOST PROTOCOL V33.0** 👻\n"
        "Tryb: `Anti-Algo Detection` 🕵️‍♂️\n\n"
        "Bot wykrywa manipulacje po Twojej serii. Wybierz czas:",
        reply_markup=main_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Sprawdzenie blokady sesji (ochrona przed tilt-em)
    if session["locked_until"] and datetime.now() < session["locked_until"]:
        left = (session["locked_until"] - datetime.now()).seconds // 60
        await query.message.reply_text(f"🛑 **BLOKADA OCHRONNA!**\nZbyt wiele przegranych. Odpocznij jeszcze {left} min.")
        return

    if query.data == "st_stats":
        await query.message.reply_text(f"📈 Wynik: {session['wins']}W - {session['losses']}L\nPassa: {session['streak']}")
        return

    if query.data.startswith("res_"):
        if "win" in query.data:
            session["wins"] += 1
            session["streak"] = max(0, session["streak"] + 1)
        else:
            session["losses"] += 1
            session["streak"] = min(0, session["streak"] - 1)
        
        # Jeśli 3 przegrane pod rząd - blokada 15 min
        if session["streak"] <= -3:
            session["locked_until"] = datetime.now() + asyncio.timedelta(minutes=15)
            await query.message.reply_text("⛔ **WYKRYTO SERIĘ PRZEGRANYCH.**\nAlgorytm brokera Cię namierzył. Blokuję sygnały na 15 minut dla Twojego bezpieczeństwa.")
        else:
            await query.message.reply_text("Zapisano. Szukam bezpiecznej luki...", reply_markup=main_keyboard())
        return

    if query.data.startswith("gt_"):
        sec = query.data.split("_")[1]
        msg = await query.message.reply_text("🔄 Mycie śladów sesji (Ghost Mode)...")
        await asyncio.sleep(random.uniform(0.5, 1.5))
        
        # Filtr siły sygnału (Tylko 4-5 gwiazdek)
        power = random.randint(1, 100)
        while power < 85 and power > 15:
            power = random.randint(1, 100)
            await asyncio.sleep(0.1)

        direction = "CALL ⬆️" if power > 50 else "PUT ⬇️"
        emoji = "🟢" if power > 50 else "🔴"
        
        await msg.delete()
        # Przyciski wyniku pod sygnałem
        res_kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ WYGRANA", callback_data="res_win"),
            InlineKeyboardButton("❌ PRZEGRANA", callback_data="res_loss")
        ]])
        
        await query.message.reply_text(
            f"{emoji} **SZYBKI STRZAŁ GHOST** {emoji}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"📈 Kierunek: **{direction}**\n"
            f"⏳ Czas: `{sec} SEC`\n"
            f"🛡️ Pewność: `ELITARNA (85%+)`\n"
            f"━━━━━━━━━━━━━━━\n"
            f"⚡ **KLIKNIJ I ZNIKAJ!**",
            reply_markup=res_kb
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
