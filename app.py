
import streamlit as st
import pandas as pd
from fpdf import FPDF
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

st.set_page_config(page_title="Etsy + Google SEO Dashboard", layout="wide")
st.title("Etsy + Google SEO Dashboard")
st.caption("Cloud-ready demo with sample data and a GA4 UTM builder. (PDF export uses pure-Python fpdf2)")

@st.cache_data
def load_data():
    queries = pd.read_csv("data/queries.csv")
    listings = pd.read_csv("data/listings.csv")
    opps = pd.read_csv("data/opportunities.csv")
    return queries, listings, opps

queries, listings, opps = load_data()

tab1, tab2, tab3, tab4 = st.tabs(["Opportunities", "Listings", "Exports", "UTM Builder"])

with tab1:
    st.subheader("Keyword Opportunities")
    st.dataframe(opps, use_container_width=True)

with tab2:
    st.subheader("Etsy Listings")
    st.dataframe(listings, use_container_width=True)

def export_pdf_table(df: pd.DataFrame, title: str, filename: str) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, title, ln=True)
    pdf.set_font("Helvetica", "", 10)
    # Column widths (simple auto-fit up to page width)
    page_width = pdf.w - 2 * pdf.l_margin
    col_width = page_width / len(df.columns)
    # Header
    for col in df.columns:
        pdf.cell(col_width, 8, txt=str(col)[:30], border=1)
    pdf.ln(8)
    # Rows
    for _, row in df.iterrows():
        for col in df.columns:
            txt = str(row[col])
            if len(txt) > 38:
                txt = txt[:35] + "..."
            pdf.cell(col_width, 8, txt=txt, border=1)
        pdf.ln(8)
    pdf.output(filename)
    return filename

with tab3:
    st.subheader("Export Reports")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export Opportunities PDF"):
            path = export_pdf_table(opps, "Opportunities Report", "opportunities_report.pdf")
            with open(path, "rb") as f:
                st.download_button("Download Opportunities PDF", data=f, file_name="opportunities_report.pdf")
        if st.button("Export Opportunities CSV"):
            path = "opportunities.csv"
            opps.to_csv(path, index=False)
            with open(path, "rb") as f:
                st.download_button("Download Opportunities CSV", data=f, file_name="opportunities.csv")
    with col2:
        if st.button("Export Listings CSV"):
            path = "listings.csv"
            listings.to_csv(path, index=False)
            with open(path, "rb") as f:
                st.download_button("Download Listings CSV", data=f, file_name="listings.csv")

with tab4:
    st.subheader("GA4 UTM Builder (Pinterest • Google • Instagram)")
    etsy_url = st.text_input("Etsy listing URL", placeholder="https://www.etsy.com/listing/123456789/item")
    channel = st.selectbox("Channel preset", ["Pinterest (organic)", "Pinterest Ads", "Google (organic)", "Google Ads (Search)", "Instagram (organic)", "Instagram Ads"])
    presets = {
        "Pinterest (organic)": {"source": "pinterest", "medium": "social"},
        "Pinterest Ads": {"source": "pinterest", "medium": "cpc"},
        "Google (organic)": {"source": "google", "medium": "organic"},
        "Google Ads (Search)": {"source": "google", "medium": "cpc"},
        "Instagram (organic)": {"source": "instagram", "medium": "social"},
        "Instagram Ads": {"source": "instagram", "medium": "cpc"},
    }
    colA, colB = st.columns(2)
    with colA:
        utm_source = st.text_input("utm_source", value=presets[channel]["source"])
        utm_medium = st.text_input("utm_medium", value=presets[channel]["medium"])
        utm_campaign = st.text_input("utm_campaign", placeholder="spring_launch_2025")
    with colB:
        utm_term = st.text_input("utm_term (optional)")
        utm_content = st.text_input("utm_content (optional)")

    def build_utm_url(url, source, medium, campaign, term=None, content=None):
        parts = list(urlparse(url))
        query = dict(parse_qsl(parts[4], keep_blank_values=True))
        query["utm_source"] = source
        query["utm_medium"] = medium
        query["utm_campaign"] = campaign
        if term:
            query["utm_term"] = term
        if content:
            query["utm_content"] = content
        parts[4] = urlencode(query, doseq=True)
        return urlunparse(parts)

    if st.button("Generate UTM Link"):
        if not etsy_url:
            st.warning("Please enter an Etsy URL.")
        else:
            utm_link = build_utm_url(etsy_url, utm_source, utm_medium, utm_campaign, utm_term, utm_content)
            st.code(utm_link, language="text")
            st.download_button("Download UTM Link (.txt)", data=utm_link.encode(), file_name="utm_link.txt")
