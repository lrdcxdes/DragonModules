from pyrogram import Client, filters
from pyrogram.types import Message

# noinspection PyUnresolvedReferences
from utils.misc import modules_help, prefix
from utils.scripts import import_library, format_exc
from utils.db import db
import ftplib

ftplib = import_library('ftplib')


# noinspection PyPep8Naming
class config:
    ip = db.get('lordcodes.filezilla', 'ip', '89.187.169.58')
    username = db.get('lordcodes.filezilla', 'username', 'lord')
    password = db.get('lordcodes.filezilla', 'password', 'lordik228')


@Client.on_message(filters.command("upload", prefix))
async def filezilla(client: Client, message: Message):
    await message.edit('<b>Connecting...</b>')
    session = ftplib.FTP(config.ip, config.username, config.password)
    filename = 'downloads/' + message.document.file_name
    await message.edit('<b>Downloading file</b>')
    await message.download(filename)
    file = open(filename, 'rb')
    await message.edit('<b>Uploading file</b>')
    session.cwd('/www/raw.lordcodes.cf/')
    session.storbinary(f'STOR {filename}', file)
    file.close()
    session.quit()
    return await message.edit('<b>Module uploaded...</b>')


@Client.on_message(filters.command("upload", prefix))
async def filezilla(client: Client, message: Message):
    await message.edit('<b>Connecting...</b>')
    session = ftplib.FTP(config.ip, config.username, config.password)
    filename = 'downloads/' + message.document.file_name
    await message.edit('<b>Downloading </b>')
    await message.download(filename)
    file = open(filename, 'rb')
    session.cwd('/www/lordcodes.cf/')
    session.storbinary(f'STOR {filename}', file)
    file.close()
    session.quit()


modules_help['filezilla'] = {
    'upload [file or reply]': 'Uploads a file to site.',
    'download [name]': 'Downloads a module from site.',
}
