# NY PL & CPL Flashcards (Flask PWA)

This repo is ready to deploy on **Render** (recommended), **Railway**, or similar PaaS.

## Local run
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Deploy to Render (free tier works)
1. Create a new GitHub repo and push these files.
2. On https://render.com, create a **Web Service** → connect your repo.
3. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -b 0.0.0.0:$PORT app:app`
   - **Environment:** Python
4. Click Deploy. Render gives you an HTTPS URL like `https://ny-law-cards.onrender.com` (PWA requires HTTPS).

### Notes
- `Procfile` is included for Procfile-based platforms.
- Service worker is served from `/service-worker.js` and will work over HTTPS in production.
