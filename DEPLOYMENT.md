# 🚀 Deployment Guide for Streamlit Cloud

## Quick Deployment Steps

### 1. Push to GitHub

Make sure your code is pushed to a GitHub repository with all these files:
- `app.py`
- `requirements.txt`
- `runtime.txt`
- `packages.txt`
- `.python-version`
- `.streamlit/config.toml`
- All `src/` files

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Click "New app"
3. Connect your GitHub repository
4. Select:
   - Repository: `your-username/your-repo-name`
   - Branch: `main` (or your default branch)
   - Main file path: `app.py`
5. Click **Advanced settings** → set **Python version** to **3.11** (required for CrewAI)
6. Click "Deploy"

> **Critical:** Streamlit Community Cloud does **not** use `runtime.txt` or `.python-version`.
> You must set Python in **Advanced settings** (or App settings → General → Python version).
> If the build uses Python 3.14, `crewai==0.28.8` will fail with "No matching distribution found".

### 3. Add Secrets

After deployment, click "Manage app" → "Settings" → "Secrets" and add:

```toml
OPENROUTER_API_KEY = "sk-or-v1-your-actual-key-here"
OPENROUTER_MODEL = "openai/gpt-4o-mini"

SERPER_API_KEY = "your-serpapi-key-here"

OPENWEATHER_API_KEY = "your-openweather-key-here"

VECTOR_STORE_PATH = "./vector_store"

CREWAI_TRACING_ENABLED = "false"
```

**Important:** Use your actual API keys from:
- OpenRouter: https://openrouter.ai/keys
- SerpApi: https://serpapi.com/dashboard
- OpenWeather: https://openweathermap.org/api

### 4. Resource Settings (Optional)

If the app needs more resources:
1. Go to "Settings" → "Resource limits"
2. Upgrade to a higher tier if needed

## Files Explained

### Python version (Streamlit UI only)
Set **Python 3.11** in Community Cloud Advanced / App settings.
`runtime.txt` and `.python-version` are kept for local/docs only — Cloud ignores them.

### `requirements.txt`
Pinned versions for:
- CrewAI 0.28.8 (requires Python `>=3.10,<3.14`)
- Streamlit 1.31.0
- ChromaDB 0.4.22 (compatible with Python 3.11)
- Pydantic 1.10.13 (compatible version)

### `packages.txt`
System-level dependencies for building native extensions

### `.streamlit/config.toml`
Streamlit server configuration

## Troubleshooting

### Error: "No matching distribution found for crewai==0.28.8"
**Cause:** Build is on Python 3.14 (or outside 3.10–3.13). Pip then only shows old crewai wheels.
**Solution:**
1. Open the app → ⋮ menu → **Settings** → **General**
2. Set **Python version** to **3.11** (or 3.12)
3. **Reboot** / redeploy and confirm logs show `Python 3.11.x` before `pip install`

### Error: "unable to infer type for attribute"
**Solution:** Use Python 3.11 in Streamlit Cloud settings (not Python 3.14)

### Error: "Module not found"
**Solution:** Check that all dependencies are in `requirements.txt`

### Error: "API key not found"
**Solution:** Add secrets in Streamlit Cloud settings

### Error: "Out of memory"
**Solution:** 
- Reduce `CHUNK_SIZE` in `src/config.py`
- Upgrade to a higher resource tier
- Use a lighter model (gpt-4o-mini instead of gpt-4o)

## Free Tier Limits

Streamlit Community Cloud free tier includes:
- 1 GB RAM
- 1 CPU core
- Limited to 1 concurrent user for free apps

For production apps with more users, consider:
- Streamlit Cloud paid tiers
- Self-hosting on AWS/GCP/Azure
- Using Docker deployment

## Local Testing

Before deploying, test locally:

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

## Alternative Deployment Options

### Docker
See `Dockerfile` (if created) for containerized deployment

### Heroku
1. Add `Procfile`: `web: streamlit run app.py`
2. Add `setup.sh` for configuration
3. Deploy via Heroku CLI

### AWS/GCP/Azure
Use their app hosting services with the same configuration files

---

## Support

For deployment issues:
- Streamlit Community Forum: https://discuss.streamlit.io/
- CrewAI Discord: https://discord.gg/crewai
- This repo's Issues page
