from vkapi import VkApiResponseException
from .. import utils
from ..objects import dp, Event


@dp.event_handle(dp.Methods.ADD_USER)
def add_user(event: Event) -> str:
    user = event.api('users.get', user_ids=event.obj['user_id'])[0]
    message = f"💚 Добавляю пользователя [id{user['id']}|{user['first_name']} {user['last_name']}]"

    message_id = utils.new_message(event.api, event.chat.peer_id, message=message)

    try:
        event.api('messages.addChatUser', chat_id=event.chat.id, user_id=user['id'])
        message = f"✅ Пользователь [id{user['id']}|{user['first_name']} {user['last_name']}] добавлен в беседу."
    except VkApiResponseException as e:
        if e.error_code == 15:
            message = f"❗ Не удалось добавить пользователя [id{user['id']}|{user['first_name']} {user['last_name']}].\n" \
                      f"Нет доступа.\n Возможно, он не в моих друзьях или он уже в беседе."
        else:
            message = f"❗ Не удалось добавить пользователя [id{user['id']}|{user['first_name']} {user['last_name']}].\n" \
                      f"Ошибка ВК.\n{e.error_msg}"
    except:
        message = f"❗ Не удалось добавить пользователя [id{user['id']}|{user['first_name']} {user['last_name']}].\n" \
                  f"Произошла неизвестная ошибка."
    utils.edit_message(event.api, event.chat.peer_id, message_id, message=message)
    return "ok"
