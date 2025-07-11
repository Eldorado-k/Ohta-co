from pyrogram import Client, filters

from .. import everyone, sudo_users
from ..utils.database.access_db import db
from ..utils.helper import check_chat, output


@Client.on_message(filters.command('addchat'))
async def addchat(client, message):
    c = await check_chat(message, chat='Owner')
    if not c:
        return
    user_id = get_id(message)
    auth = await db.get_chat()
    if user_id in everyone:
        await reply_already_auth(message)
        return
    elif str(user_id) in auth:
        await reply_already_auth(message)
        return
    else:
        auth += ' ' + str(user_id)
        await db.set_chat(auth)
        await message.reply_text('Ajouté aux groupes d\'authentification ! ID : <code>{}</code>'.format(user_id))


@Client.on_message(filters.command('addsudo'))
async def addsudo(client, message):
    c = await check_chat(message, chat='Owner')
    if not c:
        return
    user_id = get_id(message)
    auth = await db.get_sudo()
    if user_id in sudo_users:
        await reply_already_auth(message)
        return
    elif str(user_id) in auth:
        await reply_already_auth(message)
        return
    else:
        auth += ' ' + str(user_id)
        await db.set_sudo(auth)
        await message.reply_text('Ajouté aux groupe des utilisateurs privilégiés ! ID : <code>{}</code>'.format(user_id))



@Client.on_message(filters.command('rmchat'))
async def rmchat(client, message):
    c = await check_chat(message, chat='Owner')
    if not c:
        return
    user_id = get_id(message)
    check = await db.get_chat()
    if str(user_id) in check:
        user_id = ' ' + str(user_id)
        auth = check.replace(user_id, '')
        await db.set_chat(auth)
        await message.reply_text('Supprimé des groupes d\'authentification ! ID : <code>{}</code>'.format(user_id))
        return
    elif user_id in everyone:
        await message.reply_text('Suppression de la configuration d\'authentification non supportée (À faire) !')
        return
    else:
       await message.reply_text('Le chat n\'est pas encore authentifié !')


@Client.on_message(filters.command('rmsudo'))
async def rmsudo(client, message):
    c = await check_chat(message, chat='Owner')
    if not c:
        return
    user_id = get_id(message)
    check = await db.get_sudo()
    if str(user_id) in check:
        user_id = ' ' + str(user_id)
        auth = check.replace(user_id, '')
        await db.set_sudo(auth)
        await message.reply_text('Supprimé des groupes d\'authentification ! ID : <code>{}</code>'.format(user_id))
        return
    elif user_id in everyone:
        await message.reply_text('Suppression de la configuration d\'authentification non supportée (À faire) !')
        return
    else:
        await message.reply_text('Le chat n\'est pas encore authentifié !')


async def reply_already_auth(message):
    if message.reply_to_message:
        await message.reply(text='Ils sont déjà dans les utilisateurs authentifiés...')
        return
    elif not message.reply_to_message and len(message.command) != 1:
        await message.reply(text='Ils sont déjà dans les utilisateurs/groupes authentifiés...')
        return
    else:
        await message.reply(text='Ce chat est déjà dans les utilisateurs/groupes authentifiés...')
        return


def get_id(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
        user_id = message.text.split(None, 1)[1]
    else:
        user_id = message.chat.id
    return user_id
