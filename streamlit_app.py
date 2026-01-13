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
    url = "https://drive.usercontent.google.com/download?id=1x7Ho-iqwZa0i-0SYjVFYS-M_3mWUxOJt&export=download&confirm=t"
    return pd.read_csv(url, dtype=str, low_memory=False)

df = load_data()
st.write("RAW column names:")
for c in df.columns:
    st.write(repr(c))


SEARCH_COLS = ["Merk+Productnaam", "Artikelnummer", "Barcode","Artikelcode"]

DISPLAY_COLS = [
    "Artikelnummer",
    "Barcode",
    "Merk+Productnaam",
    "link website",
    "Artikelcode"
]

# ---------- HELPERS ----------
def normalize(text):
    if pd.isna(text):
        return ""
    return "".join(c.lower() for c in str(text) if c.isalnum())

# ---------- UI ----------
st.title("🔎 Disnet Link Finder")

query = st.text_input(
    "Søg efter disnet product via product navn, stregkode eller d-nummer",
    placeholder="e.g. d24091, caruba…"
)

# ---------- SEARCH ----------
if query:
    q = normalize(query)

    mask = pd.Series(False, index=df.index)

    for col in SEARCH_COLS:
        normalized_col = df[col].apply(normalize)
        mask |= normalized_col.str.contains(q, na=False)
    
    result = df.loc[mask, DISPLAY_COLS]

    st.write(f"**Found {len(result)} matching rows**")


    st.dataframe(
    result,
    use_container_width=True,
    column_config={
        "link website": st.column_config.LinkColumn(
            label="Website",
            display_text="Open link"
        )
    }
)

else:
    st.info("Indtast et søgeord for at begynde.")
