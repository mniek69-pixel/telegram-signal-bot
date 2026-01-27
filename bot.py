import os
import random
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

def time_keyboard():
    keyboard = [[
        InlineKeyboardButton("⏱ 5s", callback_data="time_5"),
        InlineKeyboardButton("⏱ 8s", callback_data="time_8"),
        InlineKeyboardButton("⏱ 15s", callback_data="time_15"),
    ]]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 **Bot Sygnałowy V2 (Analiza Trendu)**\nStatus: Aktywny 🟢\n\nWybierz czas wygaśnięcia:",
        reply_markup=time_keyboard(),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    seconds = int(query.data.split("_")[1])
    
    # Symulacja analizy (wygląda pro jak w prawdziwym terminalu)
    status_msg = await query.message.reply_text("🔍 Skanowanie rynku OTC...")
    await asyncio.sleep(1)
    await status_msg.edit_text("📊 Obliczanie wskaźnika Momentum...")
    await asyncio.sleep(1)
    
    # LOGIKA "MĄDRZEJSZEGO" BOTA
    # Generujemy 'pęd' rynku (liczba od -100 do 100)
    momentum = random.randint(-100, 100)
    
    if momentum > 0:
        signal = "CALL 🟢 (GÓRA)"
        power = random.randint(3, 5) # Silniejszy trend wzrostowy
        reason = "Silny pęd kupujących (Oversold)"
    else:
        signal = "PUT 🔴 (DÓŁ)"
        power = random.randint(3, 5)
        reason = "Presja podaży (Overbought)"

    pair = random.choice(["EUR/USD OTC"])
    stars = "⚡" * power

    await status_msg.delete() # Usuwamy komunikat o skanowaniu

    await query.message.reply_text(
        f"🚨 **SYGNAŁ ANALITYCZNY** 🚨\n\n"
        f"📊 Para: `{pair}`\n"
        f"📈 Kierunek: **{signal}**\n"
        f"⏱ Czas: `{seconds}s`\n"
        f"💪 Siła sygnału: {stars}\n"
        f"🧠 Powód: _{reason}_\n\n"
        f"🔥 **WEJDŹ TERAZ!**",
        parse_mode="Markdown",
        reply_markup=time_keyboard()
    )

if __name__ == "__main__":
    if not TOKEN:
        print("BŁĄD: Brak TOKENA!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_handler))
        print("Bot startuje...")
        app.run_polling(drop_pending_updates=True)
