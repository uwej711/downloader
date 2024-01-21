from typing import runtime_checkable, Protocol, List

from pydantic import BaseModel


class Download(BaseModel):
    filename: str
    original_url: str
    title: str
    created_timestamp: int


@runtime_checkable
class Storage(Protocol):
    def store(self, download: Download) -> None: ...
    def get(self, filename: str) -> Download: ...
    def list_all(self) -> List[Download]: ...
    def delete(self, filename: str): ...


def store_download(storage: Storage, download: Download) -> None:
    storage.store(download)


def get_download(storage: Storage, filename: str) -> Download:
    return storage.get(filename)


def list_all_downloads(storage: Storage) -> List[Download]:
    return storage.list_all()


def delete_download(storage: Storage, filename: str) -> None:
    storage.delete(filename)
