FROM arm64v8/python:3.8

RUN apt-get update && apt-get install -y chromium-driver && rm -rf /var/lib/apt/lists/*
RUN export PATH=$PATH:/usr/lib/chromium-browser/

COPY requirements.txt /

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

VOLUME /config

CMD [ "python3", "-u", "flathunt.py", "-c", "/config/config.yaml" ]