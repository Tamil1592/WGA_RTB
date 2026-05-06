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
# DATA
# -----------------------------
def generate_data():
    months = pd.date_range("2024-01-01", periods=24, freq="ME")
    templates = ["Real Estate", "Transport", "Business"]

    data = []
    for t in templates:
        for m in months:
            leads = np.random.randint(50, 200)
            conv = np.random.randint(10, 100)

            data.append({
                "Template": t,
                "Month": pd.to_datetime(m),
                "Leads": leads,
                "Conversions": conv,
                "Conversion_Rate": (conv / leads) * 100,
                "Broken_Links": np.random.randint(10, 80),
                "SEO_Score": np.random.randint(20, 90),
                "Performance": np.random.randint(30, 90)
            })

    return pd.DataFrame(data)

df = generate_data()

df["Score"] = (
    df["Conversion_Rate"] * 0.4 +
    df["SEO_Score"] * 0.2 +
    df["Performance"] * 0.2 +
    (100 - df["Broken_Links"]) * 0.2
)

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.title("⚙️ Filters")

dashboard = st.sidebar.radio(
    "Business Type",
    ["Real Estate", "Transport", "Business"]
)

time_filter = st.sidebar.radio(
    "Time Range",
    ["All", "Past 7 Days", "Past 30 Days", "Past 90 Days", "Custom Range"]
)

theme = st.sidebar.color_picker("Theme", "#1f77b4")

today = df["Month"].max()

# -----------------------------
# TIME FILTER LOGIC
# -----------------------------
if time_filter == "Past 7 Days":
    start_date = today - pd.Timedelta(days=7)
    end_date = today

elif time_filter == "Past 30 Days":
    start_date = today - pd.Timedelta(days=30)
    end_date = today

elif time_filter == "Past 90 Days":
    start_date = today - pd.Timedelta(days=90)
    end_date = today

elif time_filter == "Custom Range":
    dr = st.sidebar.date_input(
        "Select Date Range",
        (df["Month"].min().date(), df["Month"].max().date())
    )
    start_date = pd.to_datetime(dr[0])
    end_date = pd.to_datetime(dr[1])

else:
    start_date = df["Month"].min()
    end_date = df["Month"].max()

# -----------------------------
# FILTER DATA
# -----------------------------
filtered_df = df[
    (df["Template"] == dashboard) &
    (df["Month"] >= start_date) &
    (df["Month"] <= end_date)
]

if filtered_df.empty:
    st.warning("No data found for selected filters")
    st.stop()

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
    df = df.sort_values("Month").copy()
    df["t"] = range(len(df))

    model = LinearRegression()
    model.fit(df[["t"]], df[col])

    future = pd.DataFrame({
        "t": range(len(df), len(df) + 12)
    })

    future[col] = model.predict(future[["t"]])
    future["Month"] = pd.date_range(df["Month"].max(), periods=12, freq="ME")

    return future

st.subheader("🔮 Forecast")

past = filtered_df.groupby("Month")["Conversion_Rate"].mean().reset_index()

if len(past) >= 2:
    future = forecast(past, "Conversion_Rate")
    combined = pd.concat([past, future])
    st.line_chart(combined.set_index("Month"))
else:
    st.info("Not enough data for forecast")

# -----------------------------
# WEBSITE AUDIT
# -----------------------------
st.subheader("🌐 Website Audit")

url = st.text_input("Enter Website URL")

def audit(url):
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.title.string if soup.title else "Missing"
        meta = soup.find("meta", attrs={"name": "description"})

        links = soup.find_all("a")
        broken = 0

        for l in links[:15]:
            href = l.get("href")
            if href and href.startswith("http"):
                try:
                    res = requests.get(href, timeout=2)
                    if res.status_code >= 400:
                        broken += 1
                except:
                    broken += 1

        return {
            "title": title,
            "meta": bool(meta),
            "links": len(links),
            "broken": broken
        }

    except:
        return None

if st.button("Run Audit"):
    result = audit(url)

    if result:
        st.json(result)

        if not result["meta"]:
            st.warning("Missing meta description")

        if result["broken"] > 3:
            st.error("High broken links detected")

        if result["links"] < 10:
            st.info("Low internal linking structure")
    else:
        st.error("Invalid URL")

# -----------------------------
# AI INSIGHTS
# -----------------------------
st.subheader("🧠 AI Insights")

avg_conv = filtered_df["Conversion_Rate"].mean()
avg_seo = filtered_df["SEO_Score"].mean()
avg_perf = filtered_df["Performance"].mean()

score = (avg_conv * 0.5) + (avg_seo * 0.3) + (avg_perf * 0.2)

st.metric("AI Score", round(score, 2))

if score > 70:
    st.success("Strong performance 🚀")
elif score > 40:
    st.warning("Moderate performance")
else:
    st.error("Critical performance issue")

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
