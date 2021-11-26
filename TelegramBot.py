#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
                          
from config import quiz, evaluation
from stats import add

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

INTRO, Q1, A1, Q2, A2, Q3, A3, Q11, OUTRO = range(23)

sketch1 = "https://www.dropbox.com/s/l7j8t7ft7l5gnje/1.jpg?dl=0"
label = "https://www.dropbox.com/s/12benwqnccc0pig/TIA_Calc_1200x350_hello.png?dl=0"
logos = "https://www.dropbox.com/s/tnixclw8ags0l4l/TIA_Calc_1200x350_logos.png?dl=0"

keyboard = ReplyKeyboardMarkup(
    [["Художня проза"],
     ["Поезія"],
     ["Віршовані тексти пісень"],
     ["Соціально-економічні… твори"],
     ["Інша література"]],
    one_time_keyboard=True, resize_keyboard=True)

def evaluate(context):
    res = context.user_data['impact-points'] + context.user_data['pleasure-points'] + context.user_data['reputation-points'] 
    print(res)
    if res < -5:
        return "bad"
    
    if res >= -5 and res <= 5:
        return "middle"
    
    if res > 5:
        return "good"

def print_points(update, context):
        update.message.reply_text(
        """🍀 Користь для громади: <b>{}</b>\n🍦 Власне задоволення: <b>{}</b>\n👏 Репутація: <b>{}</b>""".format(context.user_data['impact-points'], context.user_data['pleasure-points'], context.user_data['reputation-points']), parse_mode=ParseMode.HTML)
    
def results_handler(update, context, Q):
    if update.message.text=="1":
        update.message.reply_text("☝"+quiz[Q]["exp1"])
        update.message.reply_text(
        """🍀 Користь для громади: <b>{}</b> ({:+})\n🍦 Власне задоволення: <b>{}</b> ({:+})\n👏 Репутація: <b>{}</b> ({:+})""".format(context.user_data['impact-points'], quiz[Q]["exp1-impact-points"], context.user_data['pleasure-points'], quiz[Q]["exp1-pleasure-points"], context.user_data['reputation-points'], quiz[Q]["exp1-reputation-points"]), parse_mode=ParseMode.HTML)
        context.user_data['impact-points'] += quiz[Q]["exp1-impact-points"]
        context.user_data['pleasure-points'] += quiz[Q]["exp1-pleasure-points"]
        context.user_data['reputation-points'] = quiz[Q]["exp1-reputation-points"]

    
    if update.message.text=="2":
        update.message.reply_text("☝"+quiz[Q]["exp2"])
        update.message.reply_text(
        """🍀 Користь для громади: <b>{}</b> ({:+})\n🍦 Власне задоволення: <b>{}</b> ({:+})\n👏 Репутація: <b>{}</b> ({:+})""".format(context.user_data['impact-points'], quiz[Q]["exp2-impact-points"], context.user_data['pleasure-points'], quiz[Q]["exp2-pleasure-points"], context.user_data['reputation-points'], quiz[Q]["exp2-reputation-points"]), parse_mode=ParseMode.HTML)
        context.user_data['impact-points'] += quiz[Q]["exp2-impact-points"]
        context.user_data['pleasure-points'] += quiz[Q]["exp2-pleasure-points"]
        context.user_data['reputation-points'] += quiz[Q]["exp2-reputation-points"]
    
    if update.message.text=="3":
        update.message.reply_text("☝"+quiz[Q]["exp3"])

        update.message.reply_text(
        """🍀 Користь для громади: <b>{}</b> ({:+})\n🍦 Власне задоволення: <b>{}</b> ({:+})\n👏 Репутація: <b>{}</b> ({:+})""".format(context.user_data['impact-points'], quiz[Q]["exp3-impact-points"], context.user_data['pleasure-points'], quiz[Q]["exp3-pleasure-points"], context.user_data['reputation-points'], quiz[Q]["exp3-reputation-points"]), parse_mode=ParseMode.HTML)
        context.user_data['impact-points'] += quiz[Q]["exp3-impact-points"]
        context.user_data['pleasure-points'] += quiz[Q]["exp3-pleasure-points"]
        context.user_data['reputation-points'] += quiz[Q]["exp3-reputation-points"]


def asker(update, Q):
    update.message.reply_text("❓" + quiz[Q]["question"] + "\n\n" + "1⃣" + quiz[Q]["a1"] + "\n\n" + "2⃣" + quiz[Q]["a2"] + "\n\n" + "3⃣" + quiz[Q]["a3"],
                              reply_markup=keyboard, one_time_keyboard=True)

def start(update, context):
    reply_keyboard = [['Почати 🎮']]
    context.user_data.clear()
    user = update.message.from_user
    try:
        add('{} {}'.format(user.first_name, user.last_name))
    except Exception:
        pass
    context.bot.send_photo(chat_id=update.message.chat_id, photo=label)


    update.message.reply_text("""Вітаємо, <b>{}</b>!
        \n<a href="https://litcentr.in.ua/index/0-50">Постановою «Про затвердження мінімальних ставок винагороди (роялті) за використання об'єктів авторського права і суміжних прав» N 72</a> Кабінет Міністр України затвердив мінімальні ставки (роялті) за, зокрема, публічне виконання, публічний показ та опублікування творів науки, літератури і мистецтва.
        \n\t\tМи підготували Кальтулятор роялті, в якому ви можете підрахувати ставку за переклад 1 умовної сторінки (18000 знаків з пробілами).""".format(user.first_name),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True), parse_mode=ParseMode.HTML,)

    return INTRO


def intro(update, context):
    context.bot.send_photo(chat_id=update.message.chat_id, photo=sketch1)
    asker(update, "Q1")
    return Q1

def q1(update, context):
    if update.message.text=="1":
        context.user_data['impact-points'] = quiz["Q1"]["exp1-impact-points"]
        context.user_data['pleasure-points'] = quiz["Q1"]["exp1-pleasure-points"]
        context.user_data['reputation-points'] = quiz["Q1"]["exp1-reputation-points"]
        update.message.reply_text(quiz["Q1"]["exp1"])
    
    if update.message.text=="2":
        context.user_data['impact-points'] = quiz["Q1"]["exp2-impact-points"]
        context.user_data['pleasure-points'] = quiz["Q1"]["exp2-pleasure-points"]
        context.user_data['reputation-points'] = quiz["Q1"]["exp2-reputation-points"]
        update.message.reply_text(quiz["Q1"]["exp2"])
    
    if update.message.text=="3":
        context.user_data['impact-points'] = quiz["Q1"]["exp3-impact-points"]
        context.user_data['pleasure-points'] = quiz["Q1"]["exp3-pleasure-points"]
        context.user_data['reputation-points'] = quiz["Q1"]["exp3-reputation-points"]
        update.message.reply_text(quiz["Q1"]["exp3"])

    print_points(update,context)

    update.message.reply_text(
        "Далі 🚀",
        reply_markup=ReplyKeyboardMarkup([["Наступне питання"]], one_time_keyboard=True, resize_keyboard=True))

    return A1

def a1(update,context):
    context.bot.send_photo(chat_id=update.message.chat_id)
    asker(update,"Q2")

    return Q2

def q2(update, context):
    results_handler(update,context,"Q2") 

    update.message.reply_text(
        "Далі 🚀",
        reply_markup=ReplyKeyboardMarkup([["Наступне питання"]], one_time_keyboard=True, resize_keyboard=True))           
    return A2

def a2(update,context):
    context.bot.send_photo(chat_id=update.message.chat_id)
    asker(update,"Q3")

    return Q3

def q3(update, context):
    results_handler(update,context,"Q3") 

    update.message.reply_text(
        "Далі 🚀",
        reply_markup=ReplyKeyboardMarkup([["Наступне питання"]], one_time_keyboard=True, resize_keyboard=True))

def a3(update,context):
    context.bot.send_photo(chat_id=update.message.chat_id)
    asker(update,"Q11")

    return Q11

def q11(update, context):
    results_handler(update,context,"Q11")

    update.message.reply_text("\n\n <b>ФІНАЛЬНИЙ РЕЗУЛЬТАТ</b>", parse_mode=ParseMode.HTML )
    update.message.reply_text(evaluation[evaluate(context)], parse_mode=ParseMode.HTML )
    print_points(update,context)
    update.message.reply_text("""\nАвторка, скетчі, код: <i>Поліна Городиська</i>
    \n\n Бот для підрахунку роялті розроблено Ініціативною групою <a href="http://litcentr.in.ua/index/0-51"><b>Translators In Action</b></a> © 2021.""", parse_mode=ParseMode.HTML)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=logos)
    update.message.reply_text("Здійснити новий прорахунок! 📟\nТисни /start ❗")

    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("2119991543:AAH6KyBW4WtGOVkI2aHc2nda1J92mBanSWM", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            INTRO: [MessageHandler(Filters.regex('^(Почати прорахунок 📟)$'), intro)],
            Q1: [MessageHandler(Filters.regex('^(1|2|3)$'), q1)],
            Q2: [MessageHandler(Filters.regex('^(1|2|3)$'), q2)],
            Q3: [MessageHandler(Filters.regex('^(1|2|3)$'), q3)],
            Q11: [MessageHandler(Filters.regex('^(1|2|3)$'), q3)],

            A1: [MessageHandler(Filters.regex('^(Наступне питання)$'), a1)],
            A2: [MessageHandler(Filters.regex('^(Наступне питання)$'), a2)],
            A3: [MessageHandler(Filters.regex('^(Наступне питання)$'), a3)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()