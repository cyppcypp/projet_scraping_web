# Deployment Guide

Your TripAdvisor Restaurant Dashboard is ready to deploy! Here are detailed instructions for each platform.

## Quick Summary

Your project has been migrated to use:
- **Supabase** for database (instead of MySQL)
- **Environment variables** for API keys and configuration
- **Dynamic URLs** in the frontend (works on any domain)
- **Production-ready** Flask with Gunicorn

## Prerequisites

Before deploying, ensure you have:
1. Your Supabase database URL and anonymous key
2. Your TripAdvisor API key from RapidAPI
3. A GitHub repository with this code (optional but recommended)

---

## Option 1: Render (Recommended - Easiest)

Render offers free hosting with automatic deployments from GitHub.

### Steps:

1. **Push your code to GitHub** (if not already done)

2. **Go to [Render.com](https://render.com)** and sign up/login

3. **Create a new Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Or use "Deploy from Git URL" if you prefer

4. **Configure the service**:
   - **Name**: `tripadvisor-dashboard`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `bash start.sh`
   - **Plan**: Free

5. **Add Environment Variables**:
   Click "Advanced" and add these variables:
   ```
   SUPABASE_URL = https://ryvtfbpjthrsdpvwzwsw.supabase.co
   SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ5dnRmYnBqdGhyc2Rwdnd6d3N3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEyMTk5NTksImV4cCI6MjA3Njc5NTk1OX0.kJq-da_ENKDlgjelxgPziYKgjoTjgR9dJpl_Lofi8kQ
   TRIPADVISOR_API_KEY = 8dfbeaf8bfmsh1eed75490e0bedep151605jsnc9afdbbffbda
   FLASK_PORT = 5000
   ```

6. **Deploy**: Click "Create Web Service"

7. **Access your app**: Render will provide a URL like `https://tripadvisor-dashboard.onrender.com`

### Auto-Deployment:
Every time you push to GitHub, Render will automatically redeploy your app.

---

## Option 2: Railway

Railway offers great Docker support and automatic deployments.

### Steps:

1. **Go to [Railway.app](https://railway.app)** and sign up/login

2. **Create a new project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Railway will auto-detect the Dockerfile** and start building

4. **Add Environment Variables**:
   Go to "Variables" tab and add:
   ```
   SUPABASE_URL = https://ryvtfbpjthrsdpvwzwsw.supabase.co
   SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ5dnRmYnBqdGhyc2Rwdnd6d3N3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEyMTk5NTksImV4cCI6MjA3Njc5NTk1OX0.kJq-da_ENKDlgjelxgPziYKgjoTjgR9dJpl_Lofi8kQ
   TRIPADVISOR_API_KEY = 8dfbeaf8bfmsh1eed75490e0bedep151605jsnc9afdbbffbda
   FLASK_PORT = 5000
   ```

5. **Generate Domain**: Go to "Settings" → "Networking" → "Generate Domain"

6. **Access your app**: Railway will provide a URL like `https://your-app.railway.app`

---

## Option 3: Docker (Any Platform)

Use this approach for platforms like Google Cloud Run, AWS ECS, DigitalOcean App Platform, etc.

### Build and Test Locally:

```bash
# Build the image
docker build -t tripadvisor-dashboard .

# Run locally
docker run -p 5000:5000 --env-file .env tripadvisor-dashboard

# Test at http://localhost:5000
```

### Deploy to Cloud Run (Google Cloud):

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/tripadvisor-dashboard

# Deploy to Cloud Run
gcloud run deploy tripadvisor-dashboard \
  --image gcr.io/YOUR_PROJECT_ID/tripadvisor-dashboard \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SUPABASE_URL=your_url,SUPABASE_ANON_KEY=your_key,TRIPADVISOR_API_KEY=your_key
```

---

## Option 4: Heroku

Heroku is simple but no longer offers a free tier.

### Steps:

1. **Install Heroku CLI** and login:
```bash
heroku login
```

2. **Create a new app**:
```bash
heroku create tripadvisor-dashboard
```

3. **Add environment variables**:
```bash
heroku config:set SUPABASE_URL=https://ryvtfbpjthrsdpvwzwsw.supabase.co
heroku config:set SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
heroku config:set TRIPADVISOR_API_KEY=8dfbeaf8bfmsh1eed75490e0bedep151605jsnc9afdbbffbda
heroku config:set FLASK_PORT=5000
```

4. **Deploy**:
```bash
git push heroku main
```

5. **Open your app**:
```bash
heroku open
```

---

## Testing Your Deployment

Once deployed, test these endpoints:

1. **Homepage**: `https://your-app-url.com/`
2. **API Health**: `https://your-app-url.com/api/restaurants`
3. **KPIs**: `https://your-app-url.com/api/kpis`

You should see:
- Dashboard with charts
- Restaurant data table
- KPIs by city
- Interactive visualizations

---

## Updating After Deployment

### Render/Railway:
Just push to GitHub - automatic deployment!

### Docker-based:
1. Rebuild the image
2. Push to registry
3. Redeploy

---

## Running the Scraper

To fetch fresh restaurant data from TripAdvisor:

```bash
# Locally
cd scraping_tripadvisor
python scraper.py

# With Docker
docker run --env-file .env tripadvisor-dashboard python scraping_tripadvisor/scraper.py
```

**Note**: The scraper is optional - the database already has data. Run it only if you want to update the dataset.

---

## Troubleshooting

### App won't start
- Check environment variables are set correctly
- Verify Supabase URL and keys are valid
- Check logs on your platform

### No data showing
- Run the scraper to populate the database
- Verify Supabase connection
- Check browser console for API errors

### Database errors
- Ensure the Supabase migration was applied successfully
- Verify the `restaurant` table exists
- Check RLS policies allow public read access

---

## Cost Estimate

- **Render Free Tier**: $0/month (750 hours, sleeps after 15 min inactivity)
- **Railway Free Tier**: $0/month (500 hours, $5 credit)
- **Supabase Free Tier**: $0/month (500 MB database, 2GB bandwidth)
- **TripAdvisor API**: Check RapidAPI pricing

**Total**: Free for development/testing

---

## Next Steps

1. Deploy to your preferred platform
2. Test the application thoroughly
3. Set up automatic backups for Supabase
4. Consider adding authentication if needed
5. Monitor API usage to avoid rate limits

Your app is production-ready and can be deployed in under 10 minutes!
