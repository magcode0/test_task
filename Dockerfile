FROM python:3.13.0b4-alpine3.20
WORKDIR /TGBOT
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python bot.py