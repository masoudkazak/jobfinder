FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


COPY ./requirements.txt .

RUN pip install --user --no-cache-dir \
    --index-url https://mirrors.aliyun.com/pypi/simple/ \
    --trusted-host mirrors.aliyun.com \
    -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=builder /root/.local /root/.local
COPY . .


ENV PATH=/root/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN grep -qxF 'clear && cat ./ecommerce.asci' /root/.bashrc || \
    echo 'clear && cat ./ecommerce.asci' >> /root/.bashrc

RUN chmod +x docker/celery/celery-entrypoint.sh
RUN chmod +x docker/django/entrypoint.sh
ENTRYPOINT ["docker/django/entrypoint.sh"]
