import logging
import os

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import google_dialogflow

logger = logging.getLogger(__name__)


def get_answer_vk(event, vk_api, google_cloud_project):
    chat_id = event.user_id
    question = event.text
    random_id = random.randint(1, 1000)
    answer = google_dialogflow.get_answer(google_cloud_project, f'vk_{chat_id}', question)

    if answer:
        vk_api.messages.send(
            user_id=chat_id,
            message=answer,
            random_id=random_id
        )
    else:
        None


def start_vk_bot(vk_community_token, google_cloud_project):
    vk_session = vk.VkApi(token=vk_community_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            get_answer_vk(event, vk_api, google_cloud_project)
    VkLongPoll(vk_session)


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    load_dotenv()

    vk_community_token = os.environ['VK_TOKEN']
    google_cloud_project = os.environ['GOOGLE_CLOUD_PROJECT']

    start_vk_bot(vk_community_token, google_cloud_project)


if __name__ == '__main__':
    main()

