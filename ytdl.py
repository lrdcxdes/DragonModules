from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from utils.scripts import format_exc, import_library
import os
from io import BytesIO


youtube_dl = import_library("youtube_dl")
YoutubeDL = youtube_dl.YoutubeDL
DownloadError = youtube_dl.utils.DownloadError
ContentTooShortError = youtube_dl.utils.ContentTooShortError
ExtractorError = youtube_dl.utils.ExtractorError
GeoRestrictedError = youtube_dl.utils.GeoRestrictedError
MaxDownloadsReached = youtube_dl.utils.MaxDownloadsReached
PostProcessingError = youtube_dl.utils.PostProcessingError
UnavailableVideoError = youtube_dl.utils.UnavailableVideoError
XAttrMetadataError = youtube_dl.utils.XAttrMetadataError

strings = {
    "name": "Youtube-Dl",
    "preparing": "<b>[YouTube-Dl]</b> Preparing...",
    "downloading": "<b>[YouTube-Dl]</b> Downloading...",
    "working": "<b>[YouTube-Dl]</b> Working...",
    "exporting": "<b>[YouTube-Dl]</b> Exporting...",
    "reply": "<b>[YouTube-Dl]</b> No link!",
    "noargs": "<b>[YouTube-Dl]</b> No args!",
    "content_too_short": "<b>[YouTube-Dl]</b> Downloading content too short!",
    "geoban": "<b>[YouTube-Dl]</b> The video is not available for your geographical location due to geographical "
              "restrictions set by the website!",
    "maxdlserr": '<b>[YouTube-Dl]</b> The download limit is as follows: " oh ahah"',
    "pperr": "<b>[YouTube-Dl]</b> Error in post-processing!",
    "noformat": "<b>[YouTube-Dl]</b> Media is not available in the requested format",
    "xameerr": "<b>[YouTube-Dl]</b> {0.code}: {0.msg}\n{0.reason}",
    "exporterr": "<b>[YouTube-Dl]</b> Error when exporting video",
    "err": "<b>[YouTube-Dl]</b> {}"
}


@Client.on_message(filters.command(["ytdl", "dlyt"], prefix) & filters.me)
async def ytdl_handler(client: Client, message: Message):
    try:
        url = message.command[1]
    except IndexError:
        return await message.edit(strings["noargs"])
    await message.edit(strings["preparing"])
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
        ],
        "outtmpl": "downloads/%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    await message.edit(strings["downloading"])
    try:
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        return await message.edit(strings["err"].format(DE))
    except ContentTooShortError:
        return await message.edit(strings["content_too_short"])
    except GeoRestrictedError:
        return await message.edit(strings["geoban"])
    except MaxDownloadsReached:
        return await message.edit(strings["maxdlserr"])
    except PostProcessingError:
        return await message.edit(strings["pperr"])
    except UnavailableVideoError:
        return await message.edit(strings["noformat"])
    except XAttrMetadataError as XAME:
        return await message.edit(strings["xameerr"].format(XAME))
    except ExtractorError:
        return await message.edit(strings["exporterr"])
    except Exception as e:
        return await message.edit('<b>[YouTube-Dl]</b>\n' + format_exc(e))

    await message.reply_video(f"downloads/{rip_data['id']}.mp4", caption=rip_data["title"])

    os.remove(f"downloads/{rip_data['id']}.mp4")

    return await message.delete()


modules_help['ytdl'] = {
    'ytdl [link]': 'Download video by link',
    'dlyt [link]': 'Download video by link',
}
