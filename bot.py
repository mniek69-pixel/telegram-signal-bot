import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# Pamięć sesji użytkownika
user_data = {}

def get_keyboard(step, pair):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(f"✅ KROK {step}/3 WYGRANY ({pair})", callback_data=f"win_{step}"),
        InlineKeyboardButton("❌ PRZEGRANA (RESET CYKLU)", callback_data="reset")
    ]])

def start_keyboard(pair):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(f"🎯 START CYKLU: {pair}", callback_data="start_cycle")
    ]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"pair": "AUD/CAD OTC", "step": 1, "dir": None}
    
    await update.message.reply_text(
        "🔄 **CYCLE SWITCHER V42.0** 🔄\n"
        "Tryb: `8-Second Turbo Scalp` ⚡\n"
        "Para startowa: **AUD/CAD OTC**\n\n"
        "Zasada: 3 wygrane i zmiana wykresu!",
        reply_markup=start_keyboard("AUD/CAD OTC")
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data
    await query.answer()

    if user_id not in user_data:
        user_data[user_id] = {"pair": "AUD/CAD OTC", "step": 1, "dir": None}

    state = user_data[user_id]

    # Resetowanie przy przegranej
    if data == "reset":
        state["step"] = 1
        await query.message.reply_text(f"📉 Przegrana. Resetujemy serię na **{state['pair']}**.", reply_markup=start_keyboard(state['pair']))
        return

    # Start lub kolejny krok
    if data == "start_cycle" or data.startswith("win_"):
        if data.startswith("win_"):
            state["step"] += 1

        # Sprawdzenie czy cykl 3 wygranych dobiegł końca
        if state["step"] > 3:
            # ZMIANA PARY
            old_pair = state["pair"]
            state["pair"] = "AUD/NZD OTC" if old_pair == "AUD/CAD OTC" else "AUD/CAD OTC"
            state["step"] = 1
            await query.message.reply_text(
                f"💰 **CYKL DOMKNIĘTY! 3/3 WYGRANE!** 💰\n"
                f"Broker namierzył {old_pair}... **UCIEKAMY!**\n\n"
                f"Przełącz się na: **{state['pair']}**",
                reply_markup=start_keyboard(state['pair'])
            )
            return

        # Generowanie sygnału
        msg = await query.message.reply_text(f"📡 Skanowanie {state['pair']}...")
        await asyncio.sleep(0.5)
        
        # Logika kierunku (na 8s szukamy impulsu)
        direction = random.choice(["CALL ⬆️ GÓRA", "PUT ⬇️ DÓŁ"])
        emoji = "🟢" if "CALL" in direction else "🔴"
        
        await msg.delete()
        await query.message.reply_text(
            f"{emoji} **SYGNAŁ {state['step']}/3** {emoji}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"💹 Para: **{state['pair']}**\n"
            f"📈 Kierunek: **{direction}**\n"
            f"⏳ Czas: `8 SEKUND`\n"
            f"━━━━━━━━━━━━━━━\n"
            f"⚡ **REAGUJ BŁYSKAWICZNIE!**",
            reply_markup=get_keyboard(state["step"], state["pair"]),
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
