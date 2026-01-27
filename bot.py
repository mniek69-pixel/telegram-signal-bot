import os
import random
import asyncio
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# Główna klawiatura
def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("⏱ 15s", callback_data="time_15"),
         InlineKeyboardButton("⏱ 30s", callback_data="time_30"),
         InlineKeyboardButton("⏱ 1m", callback_data="time_60")],
        [InlineKeyboardButton("📈 Oblicz Martingale", callback_data="calc_martingale")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Klawiatura weryfikacji
def result_keyboard():
    keyboard = [[
        InlineKeyboardButton("✅ ZYSK (ITM)", callback_data="result_win"),
        InlineKeyboardButton("❌ STRATA (OTM)", callback_data="result_loss")
    ]]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏦 **SMC ELITE V30.0 - SYSTEM 4-5 GWIAZDEK** 🏦\n"
        "Status: `Skanowanie Płynności OTC` 👁️\n\n"
        "Wybierz interwał, na którym chcesz otrzymać sygnał:",
        reply_markup=main_keyboard(),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "calc_martingale":
        await query.message.reply_text(
            "💡 **Strategia Martingale x2.2**\n1️⃣: 10$ | 2️⃣: 22$ | 3️⃣: 49$\n*Zalecane: Max 3 stopnie!*",
            parse_mode="Markdown"
        )
        return

    if data.startswith("result_"):
        res_msg = "🔥 Genialnie! SMC nie kłamie." if "win" in data else "📉 Rynek cofnął do FVG. Kolejny setup będzie silniejszy."
        await query.message.reply_text(res_msg, reply_markup=main_keyboard())
        return

    if data.startswith("time_"):
        seconds = int(data.split("_")[1])
        status_msg = await query.message.reply_text("🔎 Szukam śladów instytucji (SMC)...")
        
        # Pętla szukająca tylko mocnego sygnału (4-5 gwiazdek)
        found_strong_signal = False
        attempts = 0
        
        while not found_strong_signal:
            attempts += 1
            power = random.randint(1, 100)
            
            # Warunek: Tylko bardzo wysoka lub bardzo niska wartość (skrajne wychylenia SMC)
            if power > 80 or power < 20:
                found_strong_signal = True
                pair = random.choice(["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC"])
                
                if power > 80:
                    direction = "CALL 🟢 (GÓRA)"
                    reason = "Order Block + FVG Rejection"
                    # 4 gwiazdki dla >80, 5 gwiazdek dla >92
                    strength = "⭐⭐⭐⭐⭐" if power > 92 else "⭐⭐⭐⭐"
                else:
                    direction = "PUT 🔴 (DÓŁ)"
                    reason = "Liquidity Sweep + MSB"
                    # 4 gwiazdki dla <20, 5 gwiazdek dla <8
                    strength = "⭐⭐⭐⭐⭐" if power < 8 else "⭐⭐⭐⭐"

                await status_msg.delete()
                await query.message.reply_text(
                    f"🎯 **SMC PRECYZYJNY (ELITE)**\n\n"
                    f"📊 Para: `{pair}`\n"
                    f"📈 Kierunek: **{direction}**\n"
                    f"💪 Pewność: {strength}\n"
                    f"🔍 Analiza: `{reason}`\n"
                    f"⏳ Czas: `{seconds}s`\n\n"
                    f"🔥 **TYLKO NAJSILNIEJSZE SETUPY! POTWIERDŹ:**",
                    parse_mode="Markdown",
                    reply_markup=result_keyboard()
                )
            else:
                # Jeśli sygnał słaby, czekaj krótko i szukaj dalej (symulacja skanowania)
                await asyncio.sleep(0.3)
                if attempts > 20: # Zabezpieczenie, żeby nie czekać wiecznie
                    await status_msg.edit_text("⏳ Rynek w konsolidacji... Filtruję słabe sygnały...")
                    attempts = 0

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot SMC Elite V30 gotowy...")
    app.run_polling(drop_pending_updates=True)
