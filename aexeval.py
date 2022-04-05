from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from io import StringIO
from contextlib import redirect_stdout


async def aexec(code):
    code = f'async def __todo(): ' + \
           ''.join(f'\n {_l}' for _l in code.split('\n'))
    if 'return' in code:
        exec(code)
        return await locals()['__todo']()
    else:
        f = StringIO()
        with redirect_stdout(f):
            exec(code)
            await locals()['__todo']()
        s = f.getvalue()
        return s


@Client.on_message(filters.command(["aex", "aexec"], prefix) & filters.me)
async def example_edit(client: Client, message: Message):
    code = ' '.join(message.text.split()[1:])
    if not code:
        return await message.edit('<b>Не найден код внутри сообщения.</b>')
    try:
        s = await aexec(code)
        return await message.edit(f'<b>Code:</b>\n<code>{code.replace("<", "").replace(">", "")}</code>\n\n<b>Result'
                                  f':</b>\n<code>{s}</code>')
    except Exception as ex:
        return await message.edit(f'<b>Ошибка:</b>\n<code>{ex}</code>')


@Client.on_message(filters.command(["aev", "aeval"], prefix) & filters.me)
async def example_edit(client: Client, message: Message):
    code = ' '.join(message.text.split()[1:])
    if not code:
        return await message.edit('<b>Не найден код внутри сообщения.</b>')
    try:
        s = await eval(code)
        return await message.edit(f'<b>Expression:</b>\n<code>{code.replace("<", "").replace(">", "")}</code>\n\n<b>Result'
                                  f':</b>\n<code>{s}</code>')
    except Exception as ex:
        return await message.edit(f'<b>Ошибка:</b>\n<code>{ex}</code>')


# This adds instructions for your module
modules_help["aexeval"] = {
    "aex [code]": "Async execute python code",
    "aev [code]": "Async evaluate python code",
    "aexec [code]": "Async execute python code",
    "aeval [code]": "Async evaluate python code",
}
