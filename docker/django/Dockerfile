FROM python:3.11-slim

RUN mkdir /karsaz

WORKDIR /karsaz

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN grep -qxF 'clear && cat /karsaz/ecommerce.asci' /root/.bashrc || \
    echo 'clear && cat /karsaz/ecommerce.asci' >> /root/.bashrc && \
    apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ../../requirements.txt .

RUN pip install --no-cache-dir \
    --index-url https://mirrors.aliyun.com/pypi/simple/ \
    --trusted-host mirrors.aliyun.com \
    -r requirements.txt

COPY . .

RUN chmod +x docker/django/entrypoint.sh

ENTRYPOINT ["docker/django/entrypoint.sh"]
