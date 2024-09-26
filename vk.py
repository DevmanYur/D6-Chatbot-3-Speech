import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import google_dialogflow


def echo(event, vk_api):
    chat_id = event.user_id
    question = event.text
    random_id = random.randint(1, 1000)
    answer = google_dialogflow.get_answer(f'vk_{chat_id}', question)

    if answer:
        vk_api.messages.send(
            user_id=chat_id,
            message=answer,
            random_id=random_id
        )
    else:
        None


def start_vk_bot(vk_community_token):
    vk_session = vk.VkApi(token=vk_community_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
    VkLongPoll(vk_session)
