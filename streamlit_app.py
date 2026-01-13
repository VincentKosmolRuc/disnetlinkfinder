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

df["__search_merk_en"] = (
    df["Merk"].fillna("") + " " + df["Productnaam EN"].fillna("")
)

df["__search_merk_en_norm"] = (
    df["__search_merk_en"]
        .str.lower()
        .str.replace(r"[^a-z0-9]", "", regex=True)
)

result["Display name"] = (
    result["Merk"].fillna("") + " " + result["Productnaam EN"].fillna("")
).str.strip()

result["Display name"] = result["Display name"].where(
    result["Productnaam EN"].fillna("").str.strip() != "",
    result["Merk+Productnaam"]
)



SEARCH_COLS = ["Merk+Productnaam", "Artikelnummer", "Barcode","Artikelcode"]

DISPLAY_COLS = [
    "Artikelnummer",
    "Barcode",
    "Display name",
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

    # existing columns
    for col in SEARCH_COLS:
        if col in df.columns:
            mask |= normalize_series(df[col]).str.contains(q, na=False)

    # new combined column
    mask |= df["__search_merk_en_norm"].str.contains(q, na=False)

    result = df.loc[mask].copy()
    

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
