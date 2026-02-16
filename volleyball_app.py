import streamlit as st
import pandas as pd
from io import BytesIO

# -----------------------------
# Page config
st.set_page_config(
    page_title="Volleyball Efficiency Pivot Generator",
    layout="wide"
)

# -----------------------------
# Custom CSS for boxes and colors
st.markdown("""
<style>
.box {
    padding: 15px;
    border-radius: 10px;
    background-color: #f2f2f7;
    margin-bottom: 15px;
}
.title {
    color: #0d6efd;
    font-weight: bold;
}
.footer {
    text-align: center;
    color: gray;
    font-size: 12px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title box
with st.container():
    st.markdown('<div class="box"><h1 class="title">🏐 Volleyball Efficiency Pivot Generator</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="box">Upload your raw match CSV file. The app calculates <b>pivot-friendly efficiency</b> for each player:<br>- Serve Efficiency<br>- Reception / Pass Efficiency<br>- Attack Efficiency<br>Then download a CSV ready for Excel Pivot Table.</div>', unsafe_allow_html=True)

# -----------------------------
# File uploader box
with st.container():
    st.markdown('<div class="box"><h3>📂 Upload CSV File</h3></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["csv"])

# -----------------------------
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Keep only needed columns
    columns_needed = [
        "team", "player_name", "player_role", "skill", "skill_type",
        "evaluation", "evaluation_code", "start_zone", "end_zone", "end_subzone",
        "skill_subtype", "num_players", "num_players_numeric",
        "home_setter_position", "visiting_setter_position", "set_number"
    ]
    
    df = df[[c for c in columns_needed if c in df.columns]].copy()
    df["evaluation_code"] = df["evaluation_code"].astype(str).str.strip()

    # -----------------------------
    # Calculate efficiencies
    df["pass_eff_value"] = 0
    df["serve_eff_value"] = 0
    df["attack_eff_value"] = 0

    df.loc[df["skill"] == "Reception", "pass_eff_value"] = df.loc[df["skill"] == "Reception", "evaluation_code"].apply(
        lambda x: 1 if x in ["+", "#"] else (-1 if x in ["=", "/"] else 0)
    )

    df.loc[df["skill"] == "Serve", "serve_eff_value"] = df.loc[df["skill"] == "Serve", "evaluation_code"].apply(
        lambda x: 1 if x in ["#", "+", "/"] else (-1 if x in ["=", "-"] else 0)
    )

    df.loc[df["skill"] == "Attack", "attack_eff_value"] = df.loc[df["skill"] == "Attack", "evaluation_code"].apply(
        lambda x: 1 if x == "#" else (-1 if x in ["=", "/"] else 0)
    )

    # -----------------------------
    # Reorder columns for output
    final_columns = columns_needed + ["pass_eff_value", "serve_eff_value", "attack_eff_value"]
    df = df[final_columns]

    # -----------------------------
    # Preview box
    with st.container():
        st.markdown('<div class="box"><h3>Preview of Processed Data (first 20 rows)</h3></div>', unsafe_allow_html=True)
        st.text(df.head(20).to_string())

    # -----------------------------
    # Download box
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    with st.container():
        st.markdown('<div class="box"><h3>Download Pivot-ready CSV</h3></div>', unsafe_allow_html=True)
        st.download_button(
            label="📥 Download CSV",
            data=buffer,
            file_name="volleyball_efficiency_pivot.csv",
            mime="text/csv"
        )
else:
    st.info("Please upload a CSV file to process.")

# -----------------------------
# Footer
st.markdown("""
<style>
/* Box styling */
.box {
    padding: 15px;
    border-radius: 10px;
    background-color: #2e3c5d; /* تیره ولی متن روشن دیده شود */
    color: #f2f2f2;             /* متن روشن */
    margin-bottom: 15px;
}

/* Title color */
.title {
    color: #ffd700; /* طلایی برای عنوان */
    font-weight: bold;
}

/* Footer styling */
.footer {
    text-align: center;
    color: #cccccc;  /* خاکستری روشن برای تم تیره */
    font-size: 12px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)
