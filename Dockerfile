FROM python:3.12-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN python -m pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    python -m playwright install-deps && \
    python -m playwright install

COPY . .

CMD ["pytest", "-n", "4"]