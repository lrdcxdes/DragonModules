from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, prefix
import asyncio


class BaseDice:
    value = 0


@Client.on_message(filters.command(["dice"], prefix) & filters.me)
async def dice_text(client: Client, message: Message):
    chat = message.chat
    try:
        values = [int(val) for val in message.text.split()[1].split(',')]
        message.dice = BaseDice
        while message.dice.value not in values:
            message = (await asyncio.gather(message.delete(revoke=True),
                       client.send_dice(chat_id=chat.id)))[1]
    except Exception as e:
        await message.edit(f"<b>Произошла ошибка:</b> <code>{e}</code>")


modules_help.append(
    {"dice": [{"dice": "Используйте: <code>.dice [значения через запятую]</code> (default emoji 🎲)"}]}
)
