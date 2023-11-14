FROM python:3.9.18-slim


RUN pip install fastapi \
    requests \
    uvicorn \
    apscheduler \
    pyyaml \
    qbittorrent-api \
    loguru

# ADD . /code

COPY . /code

WORKDIR /code

CMD [ "python3", "/code/app.py" ]