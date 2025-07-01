from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

TOKEN ="     7506871066:AAEEKbt-HxEG_TpbwzkmKsylB8DKk1upVHk   "# 

CHOOSING_SHAPE, GETTING_INPUT = range(2)

def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [["دایره", "مربع"], ["مثلث", "مستطیل"]]
    update.message.reply_text(
        "سلام! 👋\nشکلی را برای محاسبه انتخاب کن:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return CHOOSING_SHAPE

def choose_shape(update: Update, context: CallbackContext) -> int:
    shape = update.message.text
    context.user_data["shape"] = shape

    if shape == "دایره":
        update.message.reply_text("لطفاً شعاع دایره را وارد کن:")
    elif shape == "مربع":
        update.message.reply_text("طول ضلع مربع را وارد کن:")
    elif shape == "مثلث":
        update.message.reply_text("طول سه ضلع مثلث را با فاصله وارد کن (مثلاً: 3 4 5):")
    elif shape == "مستطیل":
        update.message.reply_text("طول و عرض مستطیل را با فاصله وارد کن (مثلاً: 4 5):")
    else:
        update.message.reply_text("شکل نامعتبر است. لطفاً دوباره انتخاب کن.")
        return CHOOSING_SHAPE

    return GETTING_INPUT

def calculate(update: Update, context: CallbackContext) -> int:
    shape = context.user_data["shape"]
    text = update.message.text

    try:
        if shape == "دایره":
            r = float(text)
            area = 3.14 * r * r
            perimeter = 2 * 3.14 * r
        elif shape == "مربع":
            a = float(text)
            area = a * a
            perimeter = 4 * a
        elif shape == "مثلث":
            a, b, c = map(float, text.split())
            s = (a + b + c) / 2
            area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
            perimeter = a + b + c
        elif shape == "مستطیل":
            a, b = map(float, text.split())
            area = a * b
            perimeter = 2 * (a + b)
        else:
            update.message.reply_text("خطا در انتخاب شکل.")
            return ConversationHandler.END

        update.message.reply_text(
            f"📐 نتیجه:\nمساحت = {area:.2f}\nمحیط = {perimeter:.2f}",
            reply_markup=ReplyKeyboardRemove(),
        )
    except:
        update.message.reply_text("ورودی نادرست بود. لطفاً دوباره تلاش کن.")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("لغو شد ✅", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_SHAPE: [MessageHandler(Filters.text & ~Filters.command, choose_shape)],
            GETTING_INPUT: [MessageHandler(Filters.text & ~Filters.command, calculate)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
