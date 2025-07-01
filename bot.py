import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import math

TOKEN = os.getenv("TOKEN")

# مراحل گفتگو
SHAPE, DATA = range(2)

# ذخیره شکل انتخاب شده
user_shape = {}

# شروع گفتگو
def start(update: Update, context: CallbackContext):
    reply_keyboard = [['مربع', 'مستطیل'], ['دایره', 'مثلث'], ['متوازی‌الاضلاع']]
    update.message.reply_text(
        "سلام! 👋\n"
        "برای محاسبه محیط و مساحت، یکی از اشکال زیر رو انتخاب کن:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return SHAPE

# دریافت نام شکل
def shape_received(update: Update, context: CallbackContext):
    shape = update.message.text
    user_id = update.effective_user.id
    user_shape[user_id] = shape

    if shape == "مربع":
        update.message.reply_text("🔹 لطفاً طول ضلع مربع را وارد کن:")
    elif shape == "مستطیل":
        update.message.reply_text("🔹 لطفاً طول و عرض مستطیل را با فاصله وارد کن (مثلاً: 5 3):")
    elif shape == "دایره":
        update.message.reply_text("🔹 لطفاً شعاع دایره را وارد کن:")
    elif shape == "مثلث":
        update.message.reply_text("🔹 لطفاً سه ضلع مثلث را با فاصله وارد کن (مثلاً: 3 4 5):")
    elif shape == "متوازی‌الاضلاع":
        update.message.reply_text("🔹 لطفاً دو ضلع و زاویه بین‌شان را وارد کن (مثلاً: 5 4 30 یا 30r برای رادیان):")
    else:
        update.message.reply_text("شکل نامعتبر است. لطفاً دوباره انتخاب کن.")
        return SHAPE

    return DATA

# دریافت داده و محاسبه
def data_received(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    shape = user_shape.get(user_id)
    text = update.message.text.strip()
    try:
        args = text.split()
        if shape == "مربع" and len(args) == 1:
            a = float(args[0])
            p = 4 * a
            s = a * a
        elif shape == "مستطیل" and len(args) == 2:
            a, b = map(float, args)
            p = 2 * (a + b)
            s = a * b
        elif shape == "دایره" and len(args) == 1:
            r = float(args[0])
            p = 2 * math.pi * r
            s = math.pi * r * r
        elif shape == "مثلث" and len(args) == 3:
            a, b, c = map(float, args)
            p = a + b + c
            t = p / 2
            s = math.sqrt(t * (t - a) * (t - b) * (t - c))
        elif shape == "متوازی‌الاضلاع" and len(args) == 3:
            a, b = float(args[0]), float(args[1])
            angle = args[2]
            if angle.endswith('r'):
                ang = float(angle[:-1])
            else:
                ang = math.radians(float(angle))
            p = 2 * (a + b)
            s = a * b * math.sin(ang)
        else:
            update.message.reply_text("❌ تعداد داده‌ها اشتباه است.")
            return ConversationHandler.END

        update.message.reply_text(f"✅ محیط: {p:.2f}\n✅ مساحت: {s:.2f}", reply_markup=ReplyKeyboardRemove())
    except Exception as e:
        update.message.reply_text(f"❌ خطا در محاسبه: {e}", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

# لغو گفتگو
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("گفتگو لغو شد.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SHAPE: [MessageHandler(Filters.text & ~Filters.command, shape_received)],
            DATA: [MessageHandler(Filters.text & ~Filters.command, data_received)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
