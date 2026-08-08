# Streamlit Configuration

This directory contains Streamlit-specific configuration files.

## Files

### `config.toml`
General Streamlit configuration (tracked in git)
- Server settings
- Theme configuration
- Browser settings

### `secrets.toml` (NOT in git)
Your API keys and sensitive data
- ❌ Never commit this file
- ✅ Use `secrets.toml.example` as template
- ✅ Add secrets via Streamlit Cloud dashboard for deployment

### `secrets.toml.example`
Template for secrets file
- ✅ Tracked in git as a reference
- Copy to `secrets.toml` for local development

## Local Development

1. Copy the example file:
   ```bash
   copy .streamlit\secrets.toml.example .streamlit\secrets.toml
   ```

2. Edit `secrets.toml` with your actual API keys

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Streamlit Cloud Deployment

Don't create `secrets.toml` file. Instead:

1. Deploy your app to Streamlit Cloud
2. Go to app dashboard → "Manage app"
3. Click "Settings" → "Secrets"  
4. Paste your secrets in TOML format:

```toml
OPENROUTER_API_KEY = "sk-or-v1-your-key"
OPENROUTER_MODEL = "openai/gpt-4o-mini"
SERPER_API_KEY = "your-serpapi-key"
OPENWEATHER_API_KEY = "your-openweather-key"
VECTOR_STORE_PATH = "./vector_store"
CREWAI_TRACING_ENABLED = "false"
```

5. Click "Save"
6. App will automatically restart with new secrets

## Security

- `secrets.toml` is in `.gitignore` to prevent accidental commits
- Never share your API keys publicly
- Rotate keys if accidentally exposed
- Use environment-specific keys (dev vs prod)
