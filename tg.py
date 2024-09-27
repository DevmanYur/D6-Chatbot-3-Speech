import logging
import os

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import google_dialogflow
from functools import partial

logger = logging.getLogger(__name__)


def get_command_start_tg(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'Привет {user.mention_markdown_v2()}! Задай свой вопрос.',
        reply_markup=ForceReply(selective=True),
    )


def get_answer_tg(update: Update, context: CallbackContext, google_cloud_project) -> None:
    question = update.message.text
    chat_id = update.message.chat_id
    answer = google_dialogflow.get_answer(google_cloud_project, f'tg_{chat_id}', question)

    if answer:
        update.message.reply_text(text=answer)
    else:
        answer_if_empty = 'Не совсем понимаю, о чём ты'
        update.message.reply_text(text=answer_if_empty)


def start_tg_bot(telegram_token, google_cloud_project):
    get_answer = partial(get_answer_tg, google_cloud_project)
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", get_command_start_tg))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,get_answer))
    updater.start_polling()
    updater.idle()


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    load_dotenv()

    telegram_token = os.environ['TG_TOKEN']
    google_cloud_project = os.environ['GOOGLE_CLOUD_PROJECT']

    start_tg_bot(telegram_token, google_cloud_project)


if __name__ == '__main__':
    main()
