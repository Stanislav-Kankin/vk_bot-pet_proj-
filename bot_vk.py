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


def play_game():
    count = 0
    write_message(sender, 'Пиши "Погнали" чтобы начать игру!')
    write_message(sender, 'Или "Стоп" чтобы её остановить!')
    while True:
        if count == 5 or res_message == 'Стоп':
            write_message(
                sender,
                f'Спасибо за игру, твой счёт - {count}'
            )
            count = 0
        elif res_message == 'Погнали':
            write_message(sender, 'Цвет заката?')
            if res_message == 'Красный':
                count += 1
                write_message(
                    sender,
                    f'Правильно, у тебя {count} очков!'
                )
            else:
                write_message(
                    sender,
                    'Мне жналь, но ответ не верный.'
                )


authorize = VkApi(token=BOT_API_KEY)
authorize._auth_token()
longpoll = VkLongPoll(authorize)

try:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            res_message = event.text
            res_message = str(res_message).capitalize()
            sender = event.user_id
            if res_message == 'Привет':
                write_message(sender, 'Здарова!!!')
            elif res_message == 'Пока':
                write_message(sender, 'Досвидули!')
            elif res_message == 'Старт':
                play_game()
            else:
                write_message(sender, 'Я не понимаю эту строку!!!')
except KeyboardInterrupt:
    print('Выход из программы')
