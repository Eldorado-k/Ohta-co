import os
import shutil
import time
from os import execl as osexecl
from subprocess import run as srun
from sys import executable
from time import time

from psutil import (boot_time, cpu_count, cpu_percent, disk_usage,
                    net_io_counters, swap_memory, virtual_memory)
from pyrogram import Client, filters
from pyrogram.types import Message

from .. import botStartTime, download_dir, encode_dir
from ..utils.database.access_db import db
from ..utils.database.add_user import AddUserToDatabase
from ..utils.display_progress import TimeFormatter, humanbytes
from ..utils.helper import check_chat, start_but

SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def uptime():
    """ returns uptime """
    return TimeFormatter(time.time() - botStartTime)


@Client.on_message(filters.command('start'))
async def start_message(app, message):
    c = await check_chat(message, chat='Both')
    if not c:
        return
    await AddUserToDatabase(app, message)
    text = f"Salut {message.from_user.mention()}<a href='https://telegra.ph/file/11379aba315ba245ebc7b.jpg'>!</a> Je suis un encoder bot / compressor. je suis là pour t'aider et à faire des merveilles pour toi."
    await message.reply(text=text, reply_markup=start_but)


@Client.on_message(filters.command('help'))
async def help_message(app, message):
    c = await check_chat(message, chat='Both')
    if not c:
        return
    await AddUserToDatabase(app, message)
    msg = """<b>📕 Liste des Commandes</b>:

- Détection automatique des fichiers Telegram.
- /ddl - encoder via DDL
- /batch - encoder en lot
- /queue - vérifier la file d'attente
- /settings - paramètres
- /vset - voir les paramètres
- /reset - réinitialiser les paramètres
- /stats - statistiques CPU

Pour Sudo :
- /exec - Exécuter Python
- /sh - Exécuter Shell
- /vupload - upload vidéo
- /dupload - upload doc
- /gupload - upload drive
- /update - mise à jour Git
- /restart - redémarrer le bot
- /clean - nettoyer les fichiers inutiles
- /clear - vider la file d'attente
- /logs - voir les logs

Pour l'Owner :
- /addchat et /addsudo
- /rmsudo et /rmchat

Supports : <a href='https://t.me/BTZF_CHAT'>cliquez ici</a>"""
    await message.reply(text=msg, disable_web_page_preview=True, reply_markup=start_but)


@Client.on_message(filters.command('stats'))
async def show_status_count(_, event: Message):
    c = await check_chat(event, chat='Both')
    if not c:
        return
    await AddUserToDatabase(_, event)
    text = await show_status(_)
    await event.reply_text(text)


async def show_status(_):
    currentTime = TimeFormatter(time() - botStartTime)
    osUptime = TimeFormatter(time() - boot_time())
    total, used, free, disk = disk_usage('/')
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(net_io_counters().bytes_sent)
    recv = humanbytes(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    swap = swap_memory()
    swap_p = swap.percent
    memory = virtual_memory()
    mem_t = humanbytes(memory.total)
    mem_a = humanbytes(memory.available)
    mem_u = humanbytes(memory.used)
    total_users = await db.total_users_count()
    text = f"""<b>Temps de fonctionnement de</b>:
- <b>Bot :</b> {currentTime}
- <b>OS :</b> {osUptime}

<b>Disque :</b>
<b>- Total :</b> {total}
<b>- Utilisé :</b> {used}
<b>- Libre :</b> {free}

<b>UL :</b> {sent} | <b>DL :</b> {recv}
<b>CPU :</b> {cpuUsage}%

<b>Cœurs :</b>
<b>- Physiques :</b> {p_core}
<b>- Totaux :</b> {t_core}
<b>- Utilisation :</b> {swap_p}%

<b>RAM :</b> 
- <b>Total :</b> {mem_t}
- <b>Libre :</b> {mem_a}
- <b>Utilisé :</b> {mem_u}

Utilisateurs : {total_users}"""
    return text


async def showw_status(_):
    currentTime = TimeFormatter(time() - botStartTime)
    total, used, free, disk = disk_usage('/')
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpuUsage = cpu_percent(interval=0.5)
    total_users = await db.total_users_count()

    text = f"""Temps de fonctionnement du Bot : {currentTime}

Disque :
- Total : {total}
- Utilisé : {used}
- Libre : {free}
CPU : {cpuUsage}%

Utilisateurs : {total_users}"""
    return text


@Client.on_message(filters.command('clean'))
async def delete_files(_, message):
    c = await check_chat(message, chat='Sudo')
    if not c:
        return
    delete_downloads()
    await message.reply_text('Tous les fichiers inutiles ont été supprimés !')


def delete_downloads():
    dir = encode_dir
    dir2 = download_dir
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)
    for files in os.listdir(dir2):
        path = os.path.join(dir2, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)


@Client.on_message(filters.command('restart'))
async def font_message(app, message):
    c = await check_chat(message, chat='Sudo')
    if not c:
        return
    await AddUserToDatabase(app, message)
    reply = await message.reply_text('Redémarrage...')
    textx = f"Redémarrage terminé...✅"
    await reply.edit_text(textx)
    try:
        exit()
    finally:
        osexecl(executable, executable, "-m", "VideoEncoder")


@Client.on_message(filters.command('update'))
async def update_message(app, message):
    c = await check_chat(message, chat='Sudo')
    if not c:
        return
    await AddUserToDatabase(app, message)
    reply = await message.reply_text('📶 Récupération de la mise à jour...')
    textx = f"✅ Bot mis à jour"
    await reply.edit_text(textx)
    try:
        await app.stop()
    finally:
        srun([f"bash run.sh"], shell=True)
