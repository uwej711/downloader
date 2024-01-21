import os
import time
import uuid

import yt_dlp

from .model import DownloadData
from ..data import Download, Storage, store_download, delete_download


def download_and_store(storage: Storage, download_data: DownloadData) -> None:
    filename = str(uuid.uuid4())

    ydl_opts = {
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
        "outtmpl": f"downloads/{filename}"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(download_data.youtube_url)

        download = Download(
            filename=filename,
            original_url=download_data.youtube_url,
            title=info["title"],
            created_timestamp=time.time_ns()
        )

        store_download(storage, download)


def delete_file_and_download(storage: Storage, filename: str) -> None:
    delete_download(storage, filename)
    os.remove(f"downloads/{filename}.mp3")
