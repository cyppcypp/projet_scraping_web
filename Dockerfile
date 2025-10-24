FROM python:3.10-slim

WORKDIR /app

RUN mkdir -p scraping_tripadvisor/affichage scraping_tripadvisor/data

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scraping_tripadvisor/affichage/app.py scraping_tripadvisor/affichage/
COPY scraping_tripadvisor/affichage/index.html scraping_tripadvisor/affichage/
COPY scraping_tripadvisor/data/ scraping_tripadvisor/data/
COPY scraping_tripadvisor/scraper.py scraping_tripadvisor/
COPY scraping_tripadvisor/city.py scraping_tripadvisor/
COPY .env .

EXPOSE 5000

WORKDIR /app/scraping_tripadvisor/affichage

# Use shell form so $PORT is expanded correctly
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app

