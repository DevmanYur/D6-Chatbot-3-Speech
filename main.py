import os
from threading import Thread
from dotenv import load_dotenv
import logging
import tg, vk


logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    load_dotenv()

    telegram_token = os.environ['TG_TOKEN']
    vk_community_token = os.environ['VK_TOKEN']

    thread1 = Thread(target=tg.start_tg_bot(telegram_token))
    thread2 = Thread(target=vk.start_vk_bot(vk_community_token))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


if __name__ == '__main__':
    main()
