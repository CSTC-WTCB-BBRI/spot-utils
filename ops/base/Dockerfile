FROM python:3.8.16-bullseye

WORKDIR /app

COPY requirements.txt .

RUN apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get -yq dist-upgrade \
    && DEBIAN_FRONTEND=noninteractive apt-get install -qqy --no-install-recommends \
    libgl1 \
    && apt-get clean \
    && rm -rf /var/cache/apt/archives/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && truncate -s 0 /var/log/*log

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt