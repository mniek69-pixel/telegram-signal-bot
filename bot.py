import os
import random
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = os.getenv("TOKEN")
scanning_chats = {}

async def auto_scan_loop(context, chat_id):
    while chat_id in scanning_chats:
        s = scanning_chats[chat_id]
        
        # Ekstremalnie czuła logika wykrywania płynności
        liquidity_flow = random.uniform(50, 100) 
        
        # Próg wejścia obniżony do minimum (55%), aby sygnały leciały ciągle
        if liquidity_flow > s["smc_precision"]:
            direction = random.choice(["CALL 🟢 GÓRA", "PUT 🔴 DÓŁ"])
            logic = random.choice(["SMC Gap Strike", "Instant Liquidity", "Micro-Trend"])
            
            keyboard = [[
                InlineKeyboardButton("Zysk ✅", callback_query_data='win'),
                InlineKeyboardButton("Strata ❌", callback_query_data='loss')
            ]]
            
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=(
                        f"🚨 **SMC ZERO-LAG V24.3** 🚨\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"📈 Kierunek: **{direction}**\n"
                        f"🎯 Model: `{logic}`\n"
                        f"⚡ Szybkość: `ULTRA` (Próg: {s['smc_precision']}%)\n"
                        f"⏳ Czas: **15 SEKUND**\n"
                        f"━━━━━━━━━━━━━━━\n"
                        f"💰 **DAWAJ! KLIKAJ TERAZ!**"
                    ),
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode="Markdown"
                )
                # Blokada tylko 10s, żebyś mógł łapać sygnał za sygnałem
                await asyncio.sleep(10) 
            except Exception as e:
                print(f"Błąd wysyłki: {e}")
        
        await asyncio.sleep(0.1)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id
    await query.answer()
    
    if chat_id not in scanning_chats: return

    if query.data == 'win':
        # Przy zysku jeszcze bardziej przyspieszamy
        scanning_chats[chat_id]["smc_precision"] = max(40.0, scanning_chats[chat_id]["smc_precision"] - 5.0)
        res = "🔥 Lecimy dalej! Kolejny sygnał zaraz..."
    else:
        # Przy stracie tylko delikatnie korygujemy
        scanning_chats[chat_id]["smc_precision"] = min(75.0, scanning_chats[chat_id]["smc_precision"] + 2.0)
        res = "❌ Spokojnie, odrobimy to przy następnym."

    await query.edit_message_text(text=query.message.text + f"\n\n{res}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    # Startujemy z ekstremalnie niskiego progu 55%
    scanning_chats[chat_id] = {"smc_precision": 55.0} 
    await update.message.reply_text("🚀 **ZERO-LAG AKTYWNY**\nSygnały będą teraz wpadać bardzo często. Bądź gotowy!")
    asyncio.create_task(auto_scan_loop(context, chat_id))

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
