from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from io import StringIO
from contextlib import redirect_stdout
from utils.scripts import format_exc


async def aexec(code):
    code = f'async def __todo(): ' + \
           ''.join(f'\n {_l}' for _l in code.split('\n'))
    if 'return' in code:
        exec(code)
        return await locals()['__todo']()
    else:
        f = StringIO()
        exec(code)
        with redirect_stdout(f):
            await locals()['__todo']()
        s = f.getvalue()
        return s


@Client.on_message(filters.command(["aex", "aexec"], prefix) & filters.me)
async def example_edit(client: Client, message: Message):
    code = message.text.split(maxsplit=1)
    if not code:
        return await message.edit('<b>Не найден код внутри сообщения.</b>')
    try:
        await message.edit("<b>Executing...</b>")
        s = await aexec(code)
        s = s.replace('<', '').replace('>', '') if s else ''
        return await message.edit(f'<b>Code:</b>\n<code>{code.replace("<", "").replace(">", "")}</code>\n\n<b>Result'
                                  f':</b>\n<code>{s}</code>')
    except Exception as ex:
        return await message.edit(f'<b>Ошибка:</b>\n<code>{format_exc(ex)}}</code>')


@Client.on_message(filters.command(["aev", "aeval"], prefix) & filters.me)
async def example_edit(client: Client, message: Message):
    code = message.text.split(maxsplit=1)
    if not code:
        return await message.edit('<b>Не найден код внутри сообщения.</b>')
    try:
        await message.edit("<b>Executing...</b>")
        s = await eval(code)
        s = s.replace('<', '').replace('>', '') if s else ''
        return await message.edit(f'<b>Expression:</b>\n<code>{code.replace("<", "").replace(">", "")}</code>\n\n<b>Result'
                                  f':</b>\n<code>{s}</code>')
    except Exception as ex:
        return await message.edit(f'<b>Ошибка:</b>\n<code>{format_exc(ex)}</code>')


# This adds instructions for your module
modules_help["aexeval"] = {
    "aex [code]": "Async execute python code",
    "aev [code]": "Async evaluate python code",
    "aexec [code]": "Async execute python code",
    "aeval [code]": "Async evaluate python code",
}
