from vk_api import VkApi, VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from random import randint

from config import BOT_API_KEY


def write_message(sender, message, attachments=None):
    """Функция отправки сообщений пользователю"""
    authorize.method(
        'messages.send', {
            'user_id': sender,
            'message': message,
            'random_id': get_random_id(),
            'attachment': ','.join(attachments) if attachments else None
        }
    )


def play_guess_number(sender):
    """Игра  угадай случайное число"""
    secret_number = randint(1, 100)
    write_message(sender, 'Я загадал число от 1 до 100. Попробуй угадать!')
    write_message(sender, 'У тебя 5 попыток)')

    try_count = 0
    while try_count < 5:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_message = event.text
                try:
                    guess = int(user_message)
                    if guess == secret_number:
                        write_message(sender, 'Поздравляю, ты угадал число!')
                        return
                    elif guess < secret_number:
                        write_message(sender, 'Загаданное число больше!')
                    else:
                        write_message(sender, 'Загаданное число меньше!')
                    try_count += 1
                    break
                except ValueError:
                    write_message(
                        sender,
                        'Некорректный ввод. Попробуй еще раз.')

    write_message(
        sender,
        'К сожалению, ты не угадал число. Загаданное число было: {}'.format(
            secret_number
            ))


authorize = VkApi(token=BOT_API_KEY)
authorize._auth_token()
longpoll = VkLongPoll(authorize)
image = 'C:/dev/sandbox/vk_bot-pet_proj-/test.jpg'
upload = VkUpload(authorize)

try:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_message = event.text
            user_message = str(user_message).capitalize()
            sender = event.user_id
            attachments = []
            upload_image = upload.photo_messages(photos=image)[0]
            attachments.append(
                'photo{}_{}'.format(
                    upload_image['owner_id'], upload_image['id']
                ))
            if user_message == 'Привет':
                write_message(sender, 'Здарова!!!', attachments)
                write_message(sender, 'Чтобы начать игру нпиши "Играем"')
            elif user_message == 'Пока':
                write_message(sender, 'Досвидули!')
            elif user_message == 'Играем':
                play_guess_number(sender)
            else:
                write_message(sender, 'Я не понимаю эту строку!!!')
except KeyboardInterrupt:
    print('Выход из программы')
