## Streamlit deployment

This repository is a Streamlit app. Install the dependencies and run it locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

For Streamlit Community Cloud, deploy this repository with `app.py` as the main
file. Add `GROQ_API_KEY` under **Settings > Secrets** using TOML syntax:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

The same key can be provided in a local `.env` file during development.
