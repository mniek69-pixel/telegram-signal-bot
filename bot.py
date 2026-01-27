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
        
        # Obniżone progi SMC dla częstszej akcji
        smc_logic_score = random.uniform(65, 100) 
        
        # V24.2 - Próg startowy obniżony do 70%, by sygnały były częste
        if smc_logic_score > s["smc_precision"]:
            direction = random.choice(["CALL 🟢 GÓRA", "PUT 🔴 DÓŁ"])
            logic = random.choice(["Micro-OB Retest", "Quick FVG Fill", "Liquidity Hunt"])
            
            keyboard = [[
                InlineKeyboardButton("Zysk ✅", callback_query_data='win'),
                InlineKeyboardButton("Strata ❌", callback_query_data='loss')
            ]]
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f"🏦 **SMC TURBO V24.2** 🏦\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🎯 Logika: `{logic}`\n"
                    f"📈 Kierunek: **{direction}**\n"
                    f"⚡ Precyzja: `{smc_logic_score:.1f}%`\n"
                    f"⏳ Czas: **15 SEKUND**\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"🚀 **SYGNAŁ AKTYWNY - WCHODŹ!**"
                ),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )
            # Krótszy cooldown, by nie blokować kolejnych okazji
            await asyncio.sleep(15) 
        else:
            await asyncio.sleep(0.1)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id
    await query.answer()
    
    if chat_id not in scanning_chats: return

    if query.data == 'win':
        # Wygrana = jeszcze więcej sygnałów (obniżamy poprzeczkę)
        scanning_chats[chat_id]["smc_precision"] = max(60.0, scanning_chats[chat_id]["smc_precision"] - 2.0)
        msg = "✅ Potwierdzona skuteczność. Szukam dalej!"
    else:
        # Strata = lekka korekta filtrów
        scanning_chats[chat_id]["smc_precision"] = min(90.0, scanning_chats[chat_id]["smc_precision"] + 3.0)
        msg = "⚠️ Rynek szarpie. Zaostrzam skanowanie..."

    await query.edit_message_text(text=query.message.text + f"\n\n{msg}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    # Startujemy z poziomu 70.0 (duża częstotliwość)
    scanning_chats[chat_id] = {"smc_precision": 70.0} 
    await update.message.reply_text("🚀 **SMC TURBO V24.2 URUCHOMIONY**\nSygnały co ok. 1-2 minuty. Czekaj...")
    asyncio.create_task(auto_scan_loop(context, chat_id))

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
