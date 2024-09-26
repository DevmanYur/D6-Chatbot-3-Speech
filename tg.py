from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import google_dialogflow


def get_command_start_tg(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'Привет {user.mention_markdown_v2()}! Задай свой вопрос.',
        reply_markup=ForceReply(selective=True),
    )


def get_answer_tg(update: Update, context: CallbackContext) -> None:
    question = update.message.text
    chat_id = update.message.chat_id
    answer = google_dialogflow.get_answer(f'tg_{chat_id}', question)

    if answer:
        update.message.reply_text(text=answer)
    else:
        answer_if_empty = 'Не совсем понимаю, о чём ты'
        update.message.reply_text(text=answer_if_empty)


def start_tg_bot(telegram_token):
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", get_command_start_tg))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_answer_tg))
    updater.start_polling()
    updater.idle()
