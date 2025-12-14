import streamlit as st
import pandas as pd

# ---------- CONFIG ----------
st.set_page_config(
    page_title="Product Search",
    layout="wide"
)



# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    return pd.read_csv("https://drive.google.com/uc?id=1x7Ho-iqwZa0i-0SYjVFYS-M_3mWUxOJt&export=download", dtype=str, low_memory=False)

df = load_data()

SEARCH_COLS = ["Merk+Productnaam", "Artikelnummer", "Barcode"]

DISPLAY_COLS = [
    "Artikelnummer",
    "Barcode",
    "Merk+Productnaam",
    "link website"
]

# ---------- HELPERS ----------
def normalize(text):
    if pd.isna(text):
        return ""
    return "".join(c.lower() for c in str(text) if c.isalnum())

# ---------- UI ----------
st.title("🔎 Product Search")

query = st.text_input(
    "Search by product name, article number, or barcode",
    placeholder="e.g. fw759, artikelnummer, barcode…"
)

# ---------- SEARCH ----------
if query:
    q = normalize(query)

    mask = False
    for col in SEARCH_COLS:
        if col in df.columns:
            normalized_col = df[col].apply(normalize)
            mask = mask | normalized_col.str.contains(q, na=False)

    result = df[mask][DISPLAY_COLS]

    st.write(f"**Found {len(result)} matching rows**")

    # Make links clickable
    if "link website" in result.columns:
        result = result.copy()
        result["link website"] = result["link website"].apply(
            lambda x: f"[Open link]({x})" if pd.notna(x) else ""
        )

    st.dataframe(
        result,
        use_container_width=True
    )
else:
    st.info("Enter a search term to begin.")
