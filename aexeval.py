from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from io import StringIO
from contextlib import redirect_stdout
from utils.scripts import format_exc
from utils.scripts import import_library


async_eval = import_library('async-eval')
eval = async_eval.eval


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
async def aexec_handler(client: Client, message: Message):
    try:
    	code = message.text.split(maxsplit=1)[1]
    except:
    	code = ''
    if not code:
        return await message.edit('<b>Not found code to execute.</b>')
    try:
        await message.edit("<b>Executing...</b>")
        s = await aexec(code)
        s = s.replace('<', '').replace('>', '') if s else ''
        return await message.edit(f'<b>Code:</b>\n<code>{code.replace("<", "").replace(">", "")}</code>\n\n<b>Result'
                                  f':</b>\n<code>{s}</code>')
    except Exception as ex:
        return await message.edit(f'<b>Error:</b>\n<code>{format_exc(ex)}</code>')


@Client.on_message(filters.command(["aev", "aeval"], prefix) & filters.me)
async def aeval_handler(client: Client, message: Message):
    try:
    	code = message.text.split(maxsplit=1)[1]
    except:
    	code = ''
    if not code:
        return await message.edit('<b>Not found expression.</b>')
    try:
        await message.edit("<b>Executing...</b>")
        s = eval(code)
        s = s.replace('<', '').replace('>', '') if type(s) == str else s
        return await message.edit(f'<b>Expression:</b>\n<code>{code.replace("<", "").replace(">", "")}</code>\n\n<b>Result'
                                  f':</b>\n<code>{s}</code>')
    except Exception as ex:
        return await message.edit(f'<b>Error:</b>\n<code>{format_exc(ex)}</code>')


# This adds instructions for your module
modules_help["python"] = {
    "aex [code]": "Async execute python code",
    "aev [code]": "Async evaluate python code",
    "aexec [code]": "Async execute python code",
    "aeval [code]": "Async evaluate python code",
}
