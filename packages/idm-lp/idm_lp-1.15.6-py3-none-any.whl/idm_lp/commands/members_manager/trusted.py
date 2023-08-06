from vkbottle.api import UserApi
from vkbottle.framework.framework.rule import FromMe
from vkbottle.user import Blueprint, Message

from idm_lp.logger import logger_decorator
from idm_lp.database import Database, TrustedUser
from idm_lp.utils import get_ids_by_message, edit_message, get_full_name_by_member_id, generate_user_or_groups_list

user = Blueprint(
    name='trusted_blueprint'
)


@user.on.message_handler(
    FromMe(),
    text=[
        '<prefix:service_prefix> +дов [id<user_id:int>|<foo>',
        '<prefix:service_prefix> +дов [club<group_id:int>|<foo>',
        '<prefix:service_prefix> +дов https://vk.com/<domain>',
        '<prefix:service_prefix> +дов',
    ]
)
@logger_decorator
async def add_trusted_member_wrapper(
        message: Message,
        domain: str = None,
        user_id: int = None,
        group_id: int = None,
        **kwargs
):
    db = Database.get_current()
    member_id = user_id if user_id else None
    if not user_id and group_id:
        member_id = -group_id

    member_ids = await get_ids_by_message(message, member_id, domain)
    if not member_ids:
        await edit_message(
            message,
            f'⚠ Необходимо указать пользователей'
        )
        return

    member_id = member_ids[0]
    if member_id == await message.api.user_id:
        await edit_message(
            message,
            f'⚠ Нельзя занести себя в дов-лист!'
        )
        return

    if member_id > 0:
        name = f'Пользователь [id{member_id}|{await get_full_name_by_member_id(message.api, member_id)}]'
    else:
        name = f'Группа [club{abs(member_id)}|{await get_full_name_by_member_id(message.api, member_id)}]'

    if member_id in [
        muted_member.member_id
        for muted_member in db.muted_members
        if muted_member.chat_id == message.peer_id
    ]:
        await edit_message(
            message,
            f'⚠ {name} уже в довлисте'
        )
        return
    db.trusted.append(TrustedUser(user_id=member_id))
    db.save()
    await edit_message(
        message,
        f'✅ {name} добавлен в доверенные'
    )


@user.on.message_handler(
    FromMe(),
    text=[
        '<prefix:service_prefix> -дов [id<user_id:int>|<foo>',
        '<prefix:service_prefix> -дов [club<group_id:int>|<foo>',
        '<prefix:service_prefix> -дов https://vk.com/<domain>',
        '<prefix:service_prefix> -дов',
    ]
)
@logger_decorator
async def remove_trusted_member_wrapper(
        message: Message,
        domain: str = None,
        user_id: int = None,
        group_id: int = None,
        **kwargs
):
    db = Database.get_current()
    member_id = user_id if user_id else None
    if not user_id and group_id:
        member_id = -group_id

    member_ids = await get_ids_by_message(message, member_id, domain)
    if not member_ids:
        await edit_message(
            message,
            f'⚠ Необходимо указать пользователей'
        )
        return

    member_id = member_ids[0]

    if member_id > 0:
        name = f'Пользователь  [id{member_id}|{await get_full_name_by_member_id(message.api, member_id)}]'
    else:
        name = f'Группа [club{abs(member_id)}|{await get_full_name_by_member_id(message.api, member_id)}]'

    if member_id not in [
        trusted_member.user_id
        for trusted_member in db.trusted
    ]:
        await edit_message(
            message,
            f'⚠ {name} не в дов-листе'
        )
        return
    trusted = None
    for ign in db.trusted:
        if ign.user_id == member_id:
            trusted = ign
    db.trusted.remove(trusted)
    db.save()
    await edit_message(
        message,
        f'✅ {name} удален из доверенных'
    )


async def show_trusted_members(
        database: Database,
        api: UserApi
) -> str:
    user_ids = [
        trusted.user_id
        for trusted in database.trusted
        if trusted.user_id > 0
    ]
    group_ids = [
        abs(trusted.user_id)
        for trusted in database.trusted
        if trusted.user_id < 0
    ]

    if not user_ids and not group_ids:
        return "📃 Ваш дов-лист пуст"

    message = "📃 Ваш дов-лист\n"
    return await generate_user_or_groups_list(api, message, user_ids, group_ids)


@user.on.message_handler(
    FromMe(),
    text=[
        '<prefix:service_prefix> довы',
    ]
)
@logger_decorator
async def show_trusted_members_wrapper(message: Message, **kwargs):
    db = Database.get_current()
    await edit_message(
        message,
        await show_trusted_members(
            db,
            message.api
        )
    )
