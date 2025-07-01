import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    TOKEN = "توکن_واقعی_تو_رو_بعداً_اینجا_نذار، فقط برای تست فعلاً هست"

CHOOSING, TYPING = range(2)

def start(update: Update, context: CallbackContext):
    keyboard = [["دایره", "مربع"], ["مثلث", "مستطیل"]]
    update.message.reply_text(
        "سلام! ✅\nیک شکل انتخاب کن:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
    )
    return CHOOSING

def handle_shape(update: Update, context: CallbackContext):
    shape = update.message.text
    context.user_data["shape"] = shape
    prompts = {
        "دایره": "شعاع را وارد کن:",
        "مربع": "طول ضلع را وارد کن:",
        "مثلث": "سه ضلع (مثلاً: 3 4 5) را وارد کن:",
        "مستطیل": "طول و عرض (مثلاً: 4 5) را وارد کن:",
    }
    update.message.reply_text(prompts.get(shape, "شکل نامعتبر"), reply_markup=ReplyKeyboardRemove())
    return TYPING

def calculate(update: Update, context: CallbackContext):
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
            update.message.reply_text("اشتباه شکل انتخاب شد.")
            return TYPING

        update.message.reply_text(f"🎯 نتیجه:\nمساحت = {area:.2f}\nمحیط = {per:.2f}")
    except:
        update.message.reply_text("ورودی اشتباه بود، دوباره سعی کن.")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("لغو شد.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [MessageHandler(Filters.text & ~Filters.command, handle_shape)],
            TYPING: [MessageHandler(Filters.text & ~Filters.command, calculate)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dp.add_handler(conv)

    print("ربات روشن شد ✅")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
