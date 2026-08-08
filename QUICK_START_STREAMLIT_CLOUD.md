# 🚀 Quick Start: Deploy to Streamlit Cloud

## In 5 Minutes ⏱️

### Step 1: Push to GitHub (1 min)
```bash
git add .
git commit -m "Add Streamlit Cloud deployment files"
git push origin main
```

### Step 2: Deploy (2 min)
1. Go to **https://share.streamlit.io/**
2. Click **"New app"**
3. Select your repository
4. Main file: **`app.py`**
5. Click **"Deploy"**

### Step 3: Add Secrets (2 min)
1. While app is building, click **"Advanced settings"** or wait for deployment
2. Go to **"Secrets"** section
3. Paste this (with YOUR keys):

```toml
OPENROUTER_API_KEY = "sk-or-v1-YOUR-ACTUAL-KEY"
OPENROUTER_MODEL = "openai/gpt-4o-mini"
SERPER_API_KEY = "YOUR-SERPAPI-KEY"
OPENWEATHER_API_KEY = "YOUR-OPENWEATHER-KEY"
VECTOR_STORE_PATH = "./vector_store"
CREWAI_TRACING_ENABLED = "false"
```

4. Click **"Save"**

### Step 4: Done! ✅
Your app will be live at:
```
https://your-app-name.streamlit.app
```

---

## Get Your API Keys

### OpenRouter (LLM)
1. Visit: **https://openrouter.ai/keys**
2. Sign up / Log in
3. Click "Create Key"
4. Copy the key (starts with `sk-or-v1-`)

### SerpApi (Web Search)
1. Visit: **https://serpapi.com/dashboard**
2. Sign up (100 free searches/month)
3. Copy your API key

### OpenWeather (Weather Data)
1. Visit: **https://openweathermap.org/api**
2. Sign up (1000 free calls/day)
3. Go to API keys section
4. Copy your API key

---

## Troubleshooting

### App shows "Pydantic error"
✅ **Fixed!** The app now forces Python 3.11 via `runtime.txt`

### "Module not found" error
- Streamlit Cloud is still building
- Wait 2-3 minutes for installation
- Check "Manage app" → "Logs" for progress

### "API key not found"
- Click "Manage app" → "Settings" → "Secrets"
- Make sure secrets are in **TOML format** (with quotes)
- Save and wait for automatic reboot

### App is slow / times out
- Using free tier? Try upgrading to paid Streamlit Cloud
- Or use lighter model: `openai/gpt-4o-mini` instead of `gpt-4o`

---

## What's Included

✅ Multi-agent AI system  
✅ PDF analysis with RAG  
✅ Web search integration  
✅ Weather information  
✅ Chat interface  
✅ Streamlit Cloud ready  

## Free Tier Limits

- **Streamlit:** 1 app, 1GB RAM, public apps
- **SerpApi:** 100 searches/month
- **OpenWeather:** 1000 calls/day  
- **OpenRouter:** Pay per use (cheap with gpt-4o-mini)

---

**Need help?** Check `DEPLOYMENT.md` for detailed guide or `STREAMLIT_DEPLOYMENT_CHECKLIST.md` for step-by-step checklist.
