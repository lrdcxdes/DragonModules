import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

# noinspection PyUnresolvedReferences
from utils.misc import modules_help, prefix
from utils.scripts import import_library, format_exc

Image = import_library('PIL', 'pillow').Image
np = import_library('numpy')
cv2 = import_library('cv2', 'opencv-python')
imageio = import_library('imageio')


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def create_gif(offset: int, fps: int = 2):
    img = Image.open('downloads/sticker.webp')
    imageio.mimsave('downloads/video.gif', [img.rotate(-(i % 360)) for i in range(1, 361, offset)], fps=fps)


@Client.on_message(filters.command('spin', prefix) & filters.me)
async def spin_handler(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        await message.edit('<b>Reply to a sticker to spin it!</b>')
        return
    await message.edit('<b>Downloading sticker...</b>')
    await message.reply_to_message.download('sticker.webp')
    await message.edit('<b>Spinning...</b>')
    offset = int(message.command[1]) if len(message.command) > 1 else 5
    fps = int(message.command[2]) if len(message.command) > 2 else 20
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: create_gif(offset, fps))
        await message.delete()
        return await client.send_animation(chat_id=message.chat.id,
                                           animation='downloads/video.gif',
                                           reply_to_message_id=message.reply_to_message.message_id)
    except Exception as e:
        await message.reply(format_exc(e))


modules_help["spin"] = {
   "spin [offset] [fps]": "Spin sticker (Reply required)",
}
