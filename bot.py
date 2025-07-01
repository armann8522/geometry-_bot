import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    TOKEN = "7506871066:AAEEKbt-HxEG_TpbwzkmKsylB8DKk1upVHk "

CHOOSING, TYPING = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["دایره", "مربع"], ["مثلث", "مستطیل"]]
    await update.message.reply_text(
        "سلام! ✅\nیک شکل انتخاب کن:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
    )
    return CHOOSING

async def handle_shape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    shape = update.message.text
    context.user_data["shape"] = shape
    prompts = {
        "دایره": "شعاع را وارد کن:",
        "مربع": "طول ضلع را وارد کن:",
        "مثلث": "سه ضلع (مثلاً: 3 4 5) را وارد کن:",
        "مستطیل": "طول و عرض (مثلاً: 4 5) را وارد کن:",
    }
    await update.message.reply_text(prompts.get(shape, "شکل نامعتبر"), reply_markup=ReplyKeyboardRemove())
    return TYPING

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    shape = context.user_data.get("shape")
    text = update.message.text
    try:
        if shape == "دایره":
            r = float(text); area = 3.14*r*r; per = 2*3.14*r
        elif shape == "مربع":
            a = float(text); area = a*a; per = 4*a
        elif shape == "مثلث":
            a, b, c = map(float, text.split()); s=(a+b+c)/2
            area = (s*(s-a)*(s-b)*(s-c))**0.5; per = a+b+c
        elif shape == "مستطیل":
            a, b = map(float, text.split()); area = a*b; per = 2*(a+b)
        else:
            await update.message.reply_text("اشتباه شکل انتخاب شد.")
            return TYPING

        await update.message.reply_text(f"🎯 نتیجه:\nمساحت = {area:.2f}\nمحیط = {per:.2f}")
    except:
        await update.message.reply_text("ورودی اشتباه بود، دوباره سعی کن.")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لغو شد.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

from telegram.ext import ConversationHandler

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_shape)],
            TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, calculate)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)
    print("ربات روشن شد ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
