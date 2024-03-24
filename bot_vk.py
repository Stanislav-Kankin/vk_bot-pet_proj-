from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import BOT_API_KEY


def write_message(sender, message):
    authorize.method(
        'messages.send', {
            'user_id': sender,
            'message': message,
            'random_id': get_random_id()
        }
    )


authorize = VkApi(token=BOT_API_KEY)
authorize._auth_token()
longpoll = VkLongPoll(authorize)

try:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            res_message = event.text
            sender = event.user_id
            if res_message == 'Привет':
                write_message(sender, 'Здарова, заебал!')
            elif res_message == 'Пока':
                write_message(sender, 'Досвидули, хуле!')
            else:
                write_message(sender, 'Чего бл@дь? Я не понимаю эту строку!!!')
except KeyboardInterrupt:
    print('Выход с программы')
