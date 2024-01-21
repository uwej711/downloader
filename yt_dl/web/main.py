from typing import Annotated

from fastapi import BackgroundTasks, FastAPI, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.requests import Request
from starlette.status import HTTP_303_SEE_OTHER, HTTP_204_NO_CONTENT

import yt_dl.redis_storage as redis_storage
from ..data import list_all_downloads, get_download, delete_download
from ..download import DownloadData, download_and_store
from ..download.yt_download import delete_file_and_download

app = FastAPI()

templates = Jinja2Templates(directory="yt_dl/web/templates")


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def post_index(url: Annotated[str, Form()], background_tasks: BackgroundTasks):
    background_tasks.add_task(download_and_store, redis_storage, DownloadData(youtube_url=url))
    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@app.get("/downloads", response_class=HTMLResponse)
async def get_downloads(request: Request):
    downloads = list_all_downloads(redis_storage)
    return templates.TemplateResponse(
        "downloads.html",
        {
            "request": request,
            "downloads": downloads
        }
    )


@app.get("/download/{filename}", response_class=FileResponse)
async def download(filename: str):
    data = get_download(redis_storage, filename)

    if data is None:
        return None

    return FileResponse(f"downloads/{filename}.mp3", filename=f"{data.title}.mp3")


@app.post("/download/{filename}")
async def delete(filename: str):
    delete_file_and_download(redis_storage, filename)
    return RedirectResponse(url="/downloads", status_code=HTTP_303_SEE_OTHER)
