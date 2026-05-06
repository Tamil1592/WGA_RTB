import streamlit as st
import pandas as pd
import numpy as np
import hashlib
import requests
from bs4 import BeautifulSoup
from sklearn.linear_model import LinearRegression

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Smart SaaS Dashboard", layout="wide")

# -----------------------------
# LOGIN SYSTEM
# -----------------------------
USERS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest()
}

def login(user, pwd):
    return USERS.get(user) == hashlib.sha256(pwd.encode()).hexdigest()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(u, p):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

# -----------------------------
# SAMPLE DATA
# -----------------------------
def generate_data():
    # FIX: 'M' → 'ME'
    months = pd.date_range("2024-01-01", periods=24, freq="ME")
    templates = ["Real Estate", "Transport", "Business"]

    data = []
    for t in templates:
        for m in months:
            leads = np.random.randint(50, 200)
            conv = np.random.randint(10, 100)

            data.append({
                "Template": t,
                "Month": m,
                "Leads": leads,
                "Conversions": conv,
                "Conversion_Rate": (conv / leads) * 100,
                "Broken_Links": np.random.randint(10, 80),
                "SEO_Score": np.random.randint(20, 90),
                "Performance": np.random.randint(30, 90)
            })

    return pd.DataFrame(data)

df = generate_data()

# -----------------------------
# KPI SCORE
# -----------------------------
df["Score"] = (
    df["Conversion_Rate"] * 0.4 +
    df["SEO_Score"] * 0.2 +
    df["Performance"] * 0.2 +
    (100 - df["Broken_Links"]) * 0.2
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("⚙️ Controls")

dashboard = st.sidebar.radio(
    "Select Business",
    ["Real Estate", "Transport", "Business"]
)

date_range = st.sidebar.date_input(
    "Date Range",
    [df["Month"].min(), df["Month"].max()]
)

theme = st.sidebar.color_picker("Theme", "#1f77b4")

# -----------------------------
# FILTER
# -----------------------------
filtered_df = df[
    (df["Template"] == dashboard) &
    (df["Month"] >= pd.to_datetime(date_range[0])) &
    (df["Month"] <= pd.to_datetime(date_range[1]))
]

# -----------------------------
# DASHBOARD
# -----------------------------
st.title(f"📊 {dashboard} Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Leads", int(filtered_df["Leads"].sum()))
c2.metric("Conversions", int(filtered_df["Conversions"].sum()))
c3.metric("Conversion %", round(filtered_df["Conversion_Rate"].mean(), 2))
c4.metric("Score", round(filtered_df["Score"].mean(), 2))

# -----------------------------
# TREND
# -----------------------------
st.subheader("📈 Trend")

trend = filtered_df.groupby("Month")[["Conversion_Rate", "Performance"]].mean()
st.line_chart(trend)

# -----------------------------
# FORECAST
# -----------------------------
def forecast(df, col):
    df = df.sort_values("Month")
    df["t"] = range(len(df))

    model = LinearRegression()
    model.fit(df[["t"]], df[col])

    future = pd.DataFrame({
        "t": range(len(df), len(df) + 60)
    })

    future[col] = model.predict(future[["t"]])

    # FIX: 'M' → 'ME'
    future["Month"] = pd.date_range(df["Month"].max(), periods=60, freq="ME")

    return future

st.subheader("🔮 5-Year Forecast")

past = filtered_df.groupby("Month")["Conversion_Rate"].mean().reset_index()
future = forecast(past.copy(), "Conversion_Rate")

combined = pd.concat([past, future])
st.line_chart(combined.set_index("Month"))

# -----------------------------
# WEBSITE AUDIT ENGINE
# -----------------------------
st.subheader("🌐 Website Audit")

url = st.text_input("Enter Website URL")

def audit_website(url):
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.title.string if soup.title else "Missing"
        meta = soup.find("meta", attrs={"name": "description"})

        links = soup.find_all("a")
        broken = 0

        for link in links[:20]:
            href = link.get("href")
            if href and href.startswith("http"):
                try:
                    res = requests.get(href, timeout=3)
                    if res.status_code >= 400:
                        broken += 1
                except:
                    broken += 1

        return {
            "title": title,
            "meta": "Present" if meta else "Missing",
            "total_links": len(links),
            "broken_links": broken
        }

    except:
        return None

if st.button("Run Audit"):
    result = audit_website(url)

    if result:
        st.write(result)

        st.subheader("🧠 Situations & Solutions")

        if result["meta"] == "Missing":
            st.warning("❌ Situation: No meta description")
            st.success("✅ Solution: Add SEO meta tags")

        if result["broken_links"] > 5:
            st.error("❌ Situation: Many broken links")
            st.success("✅ Solution: Fix all 404 links")

        if result["total_links"] < 10:
            st.warning("❌ Situation: Low internal linking")
            st.success("✅ Solution: Add internal navigation links")
    else:
        st.error("Invalid URL or access denied")

# -----------------------------
# AI INSIGHTS
# -----------------------------
st.subheader("🤖 Smart Insights")

if filtered_df["Conversion_Rate"].mean() < 30:
    st.warning("Low conversion → Improve CTA")

if filtered_df["SEO_Score"].mean() < 50:
    st.info("SEO weak → optimize content")

if filtered_df["Performance"].mean() < 50:
    st.warning("Performance issue → optimize speed")

# -----------------------------
# THEME
# -----------------------------
st.markdown(f"""
<style>
h1, h2, h3 {{
    color: {theme};
}}
</style>
""", unsafe_allow_html=True)
