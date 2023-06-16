FROM ghcr.io/cstc-wtcb-bbri/spotutils.base:v0.0.1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt