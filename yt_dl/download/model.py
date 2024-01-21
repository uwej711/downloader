from pydantic import BaseModel


class DownloadData(BaseModel):
    youtube_url: str
