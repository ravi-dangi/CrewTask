# ✅ Streamlit Cloud Deployment Checklist

## Files Created/Updated for Deployment

### ✅ Configuration Files
- [x] `runtime.txt` - Specifies Python 3.11.11
- [x] `.python-version` - Python version file
- [x] `packages.txt` - System dependencies
- [x] `.streamlit/config.toml` - Streamlit configuration
- [x] `.streamlit/secrets.toml.example` - Secrets template

### ✅ Dependencies
- [x] `requirements.txt` - Updated with pinned versions:
  - Python 3.11 compatible
  - CrewAI 0.28.8
  - ChromaDB 0.4.22
  - Pydantic 1.10.13

### ✅ Code Updates
- [x] `src/config.py` - Added Streamlit secrets support
- [x] `src/tools/web_search_tool.py` - Added secrets fallback
- [x] `.gitignore` - Updated to allow config.toml but ignore secrets

### ✅ Documentation
- [x] `DEPLOYMENT.md` - Complete deployment guide
- [x] This checklist file

## Pre-Deployment Steps

### 1. Local Testing
```bash
# Clean install with new requirements
pip install -r requirements.txt --upgrade

# Test locally
streamlit run app.py
```

### 2. Git Commit & Push
```bash
git add .
git commit -m "Add Streamlit Cloud deployment configuration"
git push origin main
```

### 3. Prepare API Keys
Have these ready:
- [ ] OpenRouter API key
- [ ] SerpApi API key  
- [ ] OpenWeather API key

## Deployment Steps

### 1. Go to Streamlit Cloud
Visit: https://share.streamlit.io/

### 2. Deploy App
- Click "New app"
- Connect GitHub repo
- Select `app.py` as main file
- Click "Deploy"

### 3. Add Secrets
Go to "Manage app" → "Settings" → "Secrets"

Paste this (with your actual keys):
```toml
OPENROUTER_API_KEY = "sk-or-v1-your-key"
OPENROUTER_MODEL = "openai/gpt-4o-mini"
SERPER_API_KEY = "your-serpapi-key"
OPENWEATHER_API_KEY = "your-openweather-key"
VECTOR_STORE_PATH = "./vector_store"
CREWAI_TRACING_ENABLED = "false"
```

### 4. Verify Deployment
- [ ] App loads without errors
- [ ] Can upload PDF files
- [ ] Weather queries work
- [ ] Web search works
- [ ] PDF queries work (after upload)

## Common Issues & Solutions

### Issue: Pydantic ConfigError
**Cause:** Python 3.14 incompatibility  
**Solution:** ✅ Fixed with `runtime.txt` specifying Python 3.11

### Issue: ChromaDB import error
**Cause:** Version incompatibility  
**Solution:** ✅ Fixed with ChromaDB 0.4.22 pinned

### Issue: API keys not found
**Cause:** Secrets not configured  
**Solution:** Add secrets in Streamlit Cloud settings

### Issue: Out of memory
**Solution:** Use gpt-4o-mini model (cheaper and lighter)

## Post-Deployment

### Monitor Usage
- Check OpenRouter usage: https://openrouter.ai/activity
- Check SerpApi usage: https://serpapi.com/dashboard
- Monitor Streamlit app logs

### Share Your App
Your app URL will be:
`https://[your-app-name].streamlit.app`

## Cost Considerations

### Free Tiers
- Streamlit Cloud: Free (1 GB RAM, public apps)
- SerpApi: 100 searches/month free
- OpenWeather: 1000 calls/day free
- OpenRouter: Pay as you go

### Recommendations
- Use `gpt-4o-mini` for lower costs
- Set usage limits on OpenRouter
- Monitor API usage regularly

---

**Status:** Ready for deployment! 🚀

Follow the steps in `DEPLOYMENT.md` for detailed instructions.
