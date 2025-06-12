FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        netcat-openbsd \
        wget \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz && \
    tar -xzf geckodriver-v0.36.0-linux64.tar.gz -C /usr/local/bin && \
    rm geckodriver-v0.36.0-linux64.tar.gz

COPY ./requirements.txt .

RUN pip install --user --no-cache-dir \
    --index-url https://mirrors.aliyun.com/pypi/simple/ \
    --trusted-host mirrors.aliyun.com \
    -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        netcat-openbsd \
        firefox-esr \
        libgtk-3-0 \
        libdbus-glib-1-2 \
        libasound2 \
        libx11-xcb1 \
        libxt6 \
        libxss1 \
        libnss3 \
        libxrandr2 \
        libgl1 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=builder /usr/local/bin/geckodriver /usr/local/bin/geckodriver
COPY --from=builder /root/.local /root/.local
COPY . .


ENV PATH=/root/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN grep -qxF 'clear && cat ./robot.asci' /root/.bashrc || \
    echo 'clear && cat ./robot.asci' >> /root/.bashrc

RUN chmod +x docker/celery/celery-entrypoint.sh
RUN chmod +x docker/django/entrypoint.sh
ENTRYPOINT ["docker/django/entrypoint.sh"]
