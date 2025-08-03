
# Etsy + Google SEO Dashboard (Streamlit Cloud Ready, No WeasyPrint)

This version removes WeasyPrint (which requires system libraries not available on Streamlit Cloud)
and uses **fpdf2** (pure Python) for PDF export so it deploys cleanly.

## Local run
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud
1. Push this folder to a new public GitHub repo.
2. In Streamlit Cloud: Repository=`youruser/yourrepo`, Branch=`main`, Main file path=`app.py`.
3. Deploy.
