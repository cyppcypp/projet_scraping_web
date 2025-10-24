# TripAdvisor Restaurant Data Dashboard

A web application that scrapes restaurant data from TripAdvisor API and displays insights with interactive charts.

## Features

- Fetches restaurant data from TripAdvisor API for major cities
- Stores data in Supabase database
- Displays KPIs and analytics with interactive charts
- Built with Flask backend and vanilla JavaScript frontend

## Prerequisites

- Python 3.10+
- Supabase account (database already configured)
- TripAdvisor API key from RapidAPI

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
TRIPADVISOR_API_KEY=your_tripadvisor_api_key
FLASK_PORT=5000
```

3. Run the scraper (optional, to fetch fresh data):
```bash
cd scraping_tripadvisor
python scraper.py
```

4. Start the Flask application:
```bash
cd scraping_tripadvisor/affichage
python app.py
```

5. Open your browser to `http://localhost:5000`

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t tripadvisor-dashboard .
```

2. Run the container:
```bash
docker run -p 5000:5000 --env-file .env tripadvisor-dashboard
```

## Deployment Options

### Option 1: Render
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the following:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd scraping_tripadvisor/affichage && gunicorn --bind 0.0.0.0:$PORT app:app`
   - Add environment variables from `.env`

### Option 2: Railway
1. Create a new project on Railway
2. Connect your GitHub repository
3. Railway will auto-detect the Dockerfile
4. Add environment variables from `.env`

### Option 3: Docker-based platforms (Google Cloud Run, AWS ECS, etc.)
1. Build and push the Docker image to a container registry
2. Deploy the image to your preferred platform
3. Configure environment variables

## Environment Variables

- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_ANON_KEY` - Your Supabase anonymous key
- `TRIPADVISOR_API_KEY` - Your TripAdvisor API key from RapidAPI
- `FLASK_PORT` - Port for Flask app (default: 5000)

## API Endpoints

- `GET /` - Dashboard homepage
- `GET /api/restaurants` - Get all restaurants
- `GET /api/kpis` - Get KPIs by city
- `GET /api/bubble-chart` - Get bubble chart data
- `GET /api/pie-chart` - Get pie chart data
- `GET /api/line-chart` - Get line chart data

## Project Structure

```
.
├── scraping_tripadvisor/
│   ├── affichage/
│   │   ├── app.py          # Flask backend
│   │   └── index.html      # Frontend dashboard
│   ├── data/
│   │   ├── Population_by_city.csv
│   │   └── restaurants_export.csv
│   ├── scraper.py          # TripAdvisor data scraper
│   └── city.py             # City utilities
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
└── .env                   # Environment variables
```
