FROM docker.io/python:3.11-slim-bookworm

RUN apt-get update && apt-get upgrade && apt-get install -y ffmpeg

RUN useradd -rm -d /home/download -s /bin/bash -u 1001 download
RUN mkdir -p /code/downloads
RUN chown download:download /code/downloads

VOLUME /code/downloads

USER download

RUN pip install --user --no-cache-dir poetry==1.7.1

ENV PATH="/home/download/.local/bin:${PATH}"

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN poetry install

COPY yt_dl/ /code/yt_dl/

CMD ["poetry", \
    "run", \
    "uvicorn", \
    "yt_dl.web.main:app", \
    "--host", "0.0.0.0", \
    "--port", "8080"]