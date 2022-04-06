from pyrogram import Client, filters, ContinuePropagation
from pyrogram.types import Message

# noinspection PyUnresolvedReferences
from utils.misc import modules_help, prefix
from utils.scripts import format_exc

# noinspection PyUnresolvedReferences
from utils.db import db


all_filters_ = {i["word"]: i["answer"] for i in db.get_collection('lordcodes.filters').values()}


def all_filters():
    return all_filters_


async def contains_filter(_, __, m):
    return m.text and m.text.lower() in all_filters().keys()


contains = filters.create(contains_filter)


@Client.on_message(contains)
async def filters_main_handler(client: Client, message: Message):
    await message.reply(all_filters()[message.text.lower()])
    raise ContinuePropagation


@Client.on_message(filters.command(["filter"], prefix) & filters.me)
async def filter_handler(client: Client, message: Message):
    try:
        if len(message.text.split()) < 3:
            return await message.edit(
                        f"<b>Usage</b>: <code>{prefix}filter [name] [text] (Reply required)</code>"
                    )
        name = message.text.split(maxsplit=2)[1]
        if db.get('lordcodes.filters', f'filter_{name}'):
            return await message.edit(
                        f"<b>Filter</b> <code>{name}</code> already exists."
                    )
        text = message.text.split(name)[1].strip()
        if not message.reply_to_message:
            return await message.edit('<b>Reply to message</b> please.')
        elif message.reply_to_message.text:
            word = message.reply_to_message.text.lower()
        elif message.reply_to_message.caption:
            word = message.reply_to_message.caption.lower()
        else:
            return await message.edit('<b>Reply to TEXT/CAPTION message</b> please.')

        db.set('lordcodes.filters', f'filter_{name}', {'word': word,
                                                       'answer': text})
        all_filters_[word] = text
        return await message.edit(
                f"<b>Filter</b> <code>{name}</code> has been added."
            )
    except Exception as e:
        return await message.edit(format_exc(e))


@Client.on_message(filters.command(["filters"], prefix) & filters.me)
async def filters_handler(client: Client, message: Message):
    try:
        text = ''
        for index, a in enumerate(db.get_collection('lordcodes.filters').items(), start=1):
            key, item = a
            if key[:6] == 'filter':
                key = key[7:].replace('<', '').replace('>', '')
                answer = item['answer'].replace('<', '').replace('>', '')
                text += f"{index}. <code>{key}</code> — <code>{answer}</code>\n"
        text = f"<b>Filters</b>:\n\n" \
               f"{text}"
        text = text[:4096]
        return await message.edit(text)
    except Exception as e:
        return await message.edit(format_exc(e))


@Client.on_message(filters.command(["filterdel", "fdel"], prefix) & filters.me)
async def filter_del_handler(client: Client, message: Message):
    try:
        if len(message.text.split()) < 2:
            return await message.edit(
                        f"<b>Usage</b>: <code>{prefix}fdel [name]</code>"
                    )
        name = message.text.split(maxsplit=1)[1]
        value = db.get('lordcodes.filters', f'filter_{name}')
        if not value:
            return await message.edit(
                        f"<b>Filter</b> <code>{name}</code> doesn't exists."
                    )
        try:
            del all_filters_[value['word']]
        except:
            pass
        db.remove('lordcodes.filters', f'filter_{name}')
        return await message.edit(
                f"<b>Filter</b> <code>{name}</code> has been deleted."
            )
    except Exception as e:
        return await message.edit(format_exc(e))


@Client.on_message(filters.command(["fsearch"], prefix) & filters.me)
async def filter_search_handler(client: Client, message: Message):
    try:
        if len(message.text.split()) < 2:
            return await message.edit(
                        f"<b>Usage</b>: <code>{prefix}fsearch [name]</code>"
                    )
        name = message.text.split(maxsplit=1)[1]
        value = db.get('lordcodes.filters', f'filter_{name}', False)
        if not value:
            return await message.edit(f'<b>Filter</b> <code>{name}</code> doesn\'t exists.')
        return await message.edit(f'<b>Filter</b> <code>{name}</code>:\n<b>Trigger</b>: <code>{value["word"]}</code'
                                  f'>\n<b>Answer</b> '
                                  f': <code>{value["answer"]}</code>')
    except Exception as e:
        return await message.edit(format_exc(e))


modules_help['filters'] = {
    'filter [name] [text]': 'Create filter (Reply required)',
    'filters': 'List of all triggers',
    'fdel [name]': 'Delete filter by name',
    'fsearch [name]': 'Info filter by name'
}
