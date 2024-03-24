from vk_api import VkApi, VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import BOT_API_KEY


def write_message(sender, message):
    authorize.method(
        'messages.send', {
            'user_id': sender,
            'message': message,
            'random_id': get_random_id(),
            'attachments': ','.join(attachments)
        }
    )


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
                write_message(sender, 'Здарова!!!')
            elif user_message == 'Пока':
                write_message(sender, 'Досвидули!')
            else:
                write_message(sender, 'Я не понимаю эту строку!!!')
except KeyboardInterrupt:
    print('Выход из программы')
