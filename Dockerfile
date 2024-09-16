FROM python:3.9-slim

WORKDIR /web

COPY requirements.txt ./web

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x start.sh

ENV FLASK_ENV=production

CMD ["./start.sh"]