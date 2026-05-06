import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Gap Analysis Dashboard", layout="wide", page_icon="📊")

st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .block-container { padding-top: 1.5rem; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #252a3a);
        border-radius: 12px;
        padding: 18px 22px;
        border-left: 4px solid;
        margin-bottom: 10px;
    }
    .metric-card h3 { margin: 0; font-size: 13px; color: #8b95a9; font-weight: 500; letter-spacing: .05em; text-transform: uppercase; }
    .metric-card p  { margin: 6px 0 0; font-size: 26px; font-weight: 700; color: #ffffff; }
    .metric-card small { color: #8b95a9; font-size: 12px; }
    .section-title { font-size: 18px; font-weight: 700; color: #e0e4f0; margin: 18px 0 10px; padding-left: 4px; }
</style>
""", unsafe_allow_html=True)

COLORS = ["#6366f1", "#22d3ee", "#f59e0b", "#10b981", "#f43f5e",
          "#a78bfa", "#34d399", "#fb923c", "#38bdf8", "#e879f9"]

# ── Helper: KPI card ──────────────────────────────────────────────────────────
def kpi(col, title, val, sub, color):
    col.markdown(f"""<div class="metric-card" style="border-color:{color}">
        <h3>{title}</h3><p>{val}</p><small>{sub}</small></div>""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    fashion = pd.DataFrame({
        "Product ID": ["F001","F002","F003","F004","F005","F006","F007","F008","F009","F010",
                        "F011","F012","F013","F014","F015","F016","F017","F018","F019","F020"],
        "Product Name": ["Floral Wrap Dress","Slim Fit Chinos","Oversized Hoodie","Ankle Strap Heels",
                          "Denim Jacket","Printed Kurti","Cargo Shorts","Silk Blouse","Running Shoes",
                          "Leather Belt","Maxi Skirt","Polo T-Shirt","Ethnic Sherwani","Crossbody Bag",
                          "Woollen Scarf","Crop Top","Formal Trousers","Gym Leggings","Linen Shirt","Diamond Earrings"],
        "Category": ["Women / Dresses","Men / Trousers","Unisex / Tops","Women / Footwear","Unisex / Outerwear",
                      "Women / Ethnic","Men / Casual","Women / Formal","Unisex / Footwear","Accessories",
                      "Women / Bottoms","Men / Tops","Men / Ethnic","Women / Accessories","Unisex / Accessories",
                      "Women / Tops","Men / Formal","Women / Activewear","Men / Casual","Women / Jewellery"],
        "Brand": ["Zara","H&M","Nike","Aldo","Levi's","W","Puma","Mango","Adidas","Coach",
                   "Forever 21","Ralph Lauren","Manyavar","Michael Kors","Zara","H&M","Van Heusen","Lululemon","Uniqlo","Tanishq"],
        "Price": [49.99,34.99,59.99,79.99,89.99,24.99,29.99,69.99,109.99,49.99,
                   22.99,54.99,199.99,129.99,19.99,15.99,44.99,89.99,39.99,299.99],
        "Stock": [120,200,85,60,150,300,180,75,220,90,140,260,40,55,180,400,130,95,170,30],
        "Rating": [4.5,4.2,4.7,4.0,4.8,4.3,4.1,4.6,4.9,4.4,4.0,4.5,4.7,4.6,4.2,4.1,4.4,4.8,4.3,5.0],
        "Status": ["In Stock","In Stock","In Stock","Low Stock","In Stock","In Stock","In Stock","In Stock",
                    "In Stock","In Stock","In Stock","In Stock","Limited Stock","In Stock","In Stock","In Stock",
                    "In Stock","In Stock","In Stock","In Stock"]
    })

    events = pd.DataFrame({
        "Event ID": [f"E{str(i).zfill(3)}" for i in range(1, 21)],
        "Event Name": ["Annual Tech Summit 2025","Bridal Fashion Week","Startup Pitch Night","Rock Music Festival",
                        "Corporate Leadership Summit","Children's Art Carnival","Food & Wine Expo","Women in Tech Conference",
                        "Classical Dance Festival","Real Estate Expo 2025","Marathon – Run for Cause","Digital Marketing Bootcamp",
                        "Indie Film Screening","International Yoga Day","SaaS Product Launch","Heritage Walk – Old Delhi",
                        "Photography Exhibition","Annual Charity Gala","E-Sports Championship","Organic Farmers Market"],
        "Type": ["Conference","Exhibition","Networking","Concert","Workshop","Community","Exhibition","Conference",
                  "Cultural","Trade Show","Sports","Workshop","Entertainment","Wellness","Corporate","Tourism",
                  "Art","Fundraiser","Gaming","Community"],
        "City": ["Chennai","Mumbai","Bangalore","Hyderabad","Delhi","Pune","Bangalore","Hyderabad","Chennai","Mumbai",
                  "Bangalore","Delhi","Mumbai","Delhi","Bangalore","Delhi","Delhi","Mumbai","Hyderabad","Bangalore"],
        "Capacity": [500,800,150,5000,200,300,2000,400,600,1500,3000,80,120,2000,100,50,200,250,1000,400],
        "Tickets Sold": [320,650,148,3800,175,210,1600,390,420,900,2700,80,95,1800,88,50,140,230,970,350],
        "Revenue": [48000,97500,11100,190000,52500,6300,80000,58500,21000,135000,81000,32000,9500,0,0,2500,7000,115000,97000,17500],
        "Status": ["Upcoming","Confirmed","Sold Out","Upcoming","Confirmed","Upcoming","Confirmed","Almost Full",
                    "Upcoming","Confirmed","Upcoming","Sold Out","Upcoming","Free Event","Upcoming","Sold Out",
                    "Upcoming","Confirmed","Almost Full","Ongoing"]
    })
    events["Fill Rate (%)"] = (events["Tickets Sold"] / events["Capacity"] * 100).round(1)

    marketing = pd.DataFrame({
        "Campaign ID": [f"DM{str(i).zfill(3)}" for i in range(1, 21)],
        "Campaign Name": ["Summer Sale Boost","Brand Awareness – Q2","Google Search – Dresses","YouTube Pre-roll Fashion",
                           "LinkedIn B2B Events","Influencer Collab – Zara","Remarketing – Cart Abandon","Email – Festive Offers",
                           "Twitter Promoted Tweets","Snapchat AR Filter","Pinterest Shopping Ads","App Install Campaign",
                           "Event Promo – Tech Summit","SEO Content – Blog Posts","WhatsApp Broadcast","Podcast Ad – Marketing Pod",
                           "Flash Sale – 24 Hr Push","Competitor Keyword Bids","Brand Video – YouTube","Lookalike Audience Push"],
        "Platform": ["Instagram","Facebook","Google Ads","YouTube","LinkedIn","Instagram","Google Ads","Email",
                      "Twitter/X","Snapchat","Pinterest","Google UAC","Facebook","Organic","WhatsApp","Spotify",
                      "Instagram+FB","Google Ads","YouTube","Facebook"],
        "Budget": [500,2000,800,1200,600,3000,300,100,400,700,500,1500,350,200,50,800,200,600,2500,900],
        "Spend":  [480,1980,760,950,590,3000,290,100,370,680,490,1440,340,200,50,400,200,580,1200,870],
        "Impressions": [45000,210000,32000,180000,18000,500000,12000,0,60000,95000,40000,250000,28000,75000,0,12000,30000,22000,300000,85000],
        "Clicks": [1200,4200,3840,5400,720,25000,1800,8000,900,3800,2000,7500,1400,6000,3500,600,3000,2640,6000,3400],
        "CTR (%)": [2.67,2,12,3,4,5,15,28.6,1.5,4,5,3,5,8,70,5,10,12,2,4],
        "Conversions": [312,630,580,270,144,2250,360,960,90,190,400,1875,280,900,700,72,750,396,300,510],
        "Conv Rate (%)": [26,15,15.1,5,20,9,20,12,10,5,20,25,20,15,20,12,25,15,5,15],
        "ROAS": [3.9,2.8,5.1,2.1,4.5,6.7,8.2,12.5,1.8,2.3,5.5,4.2,3.5,None,9.8,2.6,11.2,4.8,1.5,4.1]
    })
    marketing["Budget Utilization (%)"] = (marketing["Spend"] / marketing["Budget"] * 100).round(1)
    return fashion, events, marketing

fashion_df, events_df, marketing_df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/48/combo-chart.png", width=40)
st.sidebar.title("Gap Analysis")
st.sidebar.markdown("---")
tab_choice = st.sidebar.radio("Navigate", ["🛍️ Fashion", "🎪 Event Management", "📣 Digital Marketing", "🔍 Gap Summary"])
st.sidebar.markdown("---")
st.sidebar.caption("Data: Web Gap Analysis Dataset · 2025")

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — FASHION
# ════════════════════════════════════════════════════════════════════════════
if tab_choice == "🛍️ Fashion":
    st.title("🛍️ Fashion – Product Intelligence")

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "Total Units in Stock",  f"{fashion_df['Stock'].sum():,}",             "across 20 products",    "#6366f1")
    kpi(c2, "Avg. Price (USD)",      f"${fashion_df['Price'].mean():.2f}",          "per product",           "#22d3ee")
    kpi(c3, "Avg. Customer Rating",  f"⭐ {fashion_df['Rating'].mean():.2f} / 5",  "20 products rated",     "#f59e0b")
    kpi(c4, "Low / Limited Stock",
        f"{fashion_df[fashion_df['Status'].isin(['Low Stock','Limited Stock'])].shape[0]} products",
        "need restock attention", "#f43f5e")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Stock by Category</div>', unsafe_allow_html=True)
        cat_stock = fashion_df.groupby("Category")["Stock"].sum().reset_index().sort_values("Stock", ascending=True)
        fig = px.bar(cat_stock, x="Stock", y="Category", orientation="h",
                     color="Stock", color_continuous_scale="Viridis", template="plotly_dark")
        fig.update_layout(coloraxis_showscale=False, paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=10,b=0), height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Price vs Rating (Bubble = Stock)</div>', unsafe_allow_html=True)
        fig2 = px.scatter(fashion_df, x="Price", y="Rating", size="Stock",
                          color="Category", hover_name="Product Name",
                          color_discrete_sequence=COLORS, template="plotly_dark")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            margin=dict(l=0,r=0,t=10,b=0), height=380, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-title">Brand Performance (Avg Rating)</div>', unsafe_allow_html=True)
        brand_rating = fashion_df.groupby("Brand")["Rating"].mean().sort_values(ascending=False).reset_index()
        fig3 = px.bar(brand_rating, x="Brand", y="Rating",
                      color="Rating", color_continuous_scale="RdYlGn", template="plotly_dark")
        fig3.update_layout(coloraxis_showscale=False, paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=10,b=0),
                            height=350, xaxis_tickangle=-40)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-title">Stock Status Breakdown</div>', unsafe_allow_html=True)
        status_counts = fashion_df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig4 = px.pie(status_counts, names="Status", values="Count",
                      color_discrete_sequence=["#10b981","#f59e0b","#f43f5e"],
                      hole=0.5, template="plotly_dark")
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=10,b=0), height=350)
        st.plotly_chart(fig4, use_container_width=True)

    # ── FIX: .bar() instead of .background_gradient() — no matplotlib needed ──
    st.markdown('<div class="section-title">Product Detail Table</div>', unsafe_allow_html=True)
    display_f = fashion_df[["Product Name","Category","Brand","Price","Stock","Rating","Status"]].copy()
    st.dataframe(
        display_f.style
                 .bar(subset=["Stock"],  color="#6366f1", vmin=0)
                 .bar(subset=["Rating"], color="#22d3ee", vmin=0, vmax=5)
                 .format({"Price": "${:.2f}", "Rating": "{:.1f}"}),
        use_container_width=True
    )


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — EVENT MANAGEMENT
# ════════════════════════════════════════════════════════════════════════════
elif tab_choice == "🎪 Event Management":
    st.title("🎪 Event Management – Performance Overview")

    total_rev  = events_df["Revenue"].sum()
    total_sold = events_df["Tickets Sold"].sum()
    total_cap  = events_df["Capacity"].sum()
    avg_fill   = events_df["Fill Rate (%)"].mean()
    sold_out   = events_df[events_df["Status"].isin(["Sold Out","Almost Full"])].shape[0]

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "Total Revenue (USD)",    f"${total_rev:,.0f}",         "across 20 events",           "#6366f1")
    kpi(c2, "Tickets Sold",           f"{total_sold:,}",            f"of {total_cap:,} capacity", "#22d3ee")
    kpi(c3, "Avg. Fill Rate",         f"{avg_fill:.1f}%",           "seats occupied",             "#f59e0b")
    kpi(c4, "Sold Out / Almost Full", f"{sold_out} events",         "high demand events",         "#10b981")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Revenue by Event (Top 10)</div>', unsafe_allow_html=True)
        top_rev = events_df[events_df["Revenue"] > 0].nlargest(10, "Revenue")
        fig = px.bar(top_rev, x="Revenue", y="Event Name", orientation="h",
                     color="Revenue", color_continuous_scale="Purples", template="plotly_dark")
        fig.update_layout(coloraxis_showscale=False, paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=10,b=0), height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Ticket Fill Rate by Event</div>', unsafe_allow_html=True)
        fill_sorted = events_df.sort_values("Fill Rate (%)", ascending=True)
        fig2 = px.bar(fill_sorted, x="Fill Rate (%)", y="Event Name", orientation="h",
                      color="Fill Rate (%)", color_continuous_scale="RdYlGn", template="plotly_dark")
        fig2.update_layout(coloraxis_showscale=False, paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=10,b=0), height=380)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-title">Revenue by City</div>', unsafe_allow_html=True)
        city_rev = events_df.groupby("City")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False)
        fig3 = px.bar(city_rev, x="City", y="Revenue",
                      color="Revenue", color_continuous_scale="Teal", template="plotly_dark")
        fig3.update_layout(coloraxis_showscale=False, paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=10,b=0), height=330)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-title">Event Type Distribution</div>', unsafe_allow_html=True)
        type_counts = events_df["Type"].value_counts().reset_index()
        type_counts.columns = ["Type", "Count"]
        fig4 = px.pie(type_counts, names="Type", values="Count",
                      color_discrete_sequence=COLORS, hole=0.4, template="plotly_dark")
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=10,b=0), height=330)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-title">Capacity vs Tickets Sold</div>', unsafe_allow_html=True)
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(name="Capacity", x=events_df["Event Name"], y=events_df["Capacity"],
                          marker_color="#6366f1", opacity=0.6))
    fig5.add_trace(go.Bar(name="Tickets Sold", x=events_df["Event Name"], y=events_df["Tickets Sold"],
                          marker_color="#22d3ee"))
    fig5.update_layout(barmode="overlay", template="plotly_dark",
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       xaxis_tickangle=-40, margin=dict(l=0,r=0,t=10,b=0), height=370)
    st.plotly_chart(fig5, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — DIGITAL MARKETING
# ════════════════════════════════════════════════════════════════════════════
elif tab_choice == "📣 Digital Marketing":
    st.title("📣 Digital Marketing – Campaign Analytics")

    total_spend = marketing_df["Spend"].sum()
    total_conv  = marketing_df["Conversions"].sum()
    total_imp   = marketing_df["Impressions"].sum()
    avg_ctr     = marketing_df["CTR (%)"].mean()

    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "Total Ad Spend (USD)", f"${total_spend:,.0f}", "across 20 campaigns", "#6366f1")
    kpi(c2, "Total Conversions",    f"{total_conv:,}",      "purchases / sign-ups", "#22d3ee")
    kpi(c3, "Total Impressions",    f"{total_imp:,}",       "ad views recorded",    "#f59e0b")
    kpi(c4, "Avg. CTR",             f"{avg_ctr:.1f}%",      "click-through rate",   "#10b981")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">ROAS by Campaign</div>', unsafe_allow_html=True)
        roas_df = marketing_df.dropna(subset=["ROAS"]).sort_values("ROAS", ascending=False)
        fig = px.bar(roas_df, x="Campaign Name", y="ROAS",
                     color="ROAS", color_continuous_scale="RdYlGn", template="plotly_dark")
        fig.add_hline(y=4, line_dash="dash", line_color="#f43f5e", annotation_text="Target ROAS = 4x")
        fig.update_layout(coloraxis_showscale=False, paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(0,0,0,0)", xaxis_tickangle=-45,
                          margin=dict(l=0,r=0,t=10,b=0), height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Conversions by Platform</div>', unsafe_allow_html=True)
        plat_conv = marketing_df.groupby("Platform")[["Conversions","Spend"]].sum().reset_index()
        plat_conv["CPA"] = (plat_conv["Spend"] / plat_conv["Conversions"]).round(2)
        fig2 = px.scatter(plat_conv, x="Spend", y="Conversions", size="Conversions",
                          color="Platform", text="Platform",
                          color_discrete_sequence=COLORS, template="plotly_dark")
        fig2.update_traces(textposition="top center")
        fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            margin=dict(l=0,r=0,t=10,b=0), height=400, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-title">Budget vs Spend (Utilization)</div>', unsafe_allow_html=True)
        util_df = marketing_df.sort_values("Budget Utilization (%)", ascending=True)
        fig3 = px.bar(util_df, x="Budget Utilization (%)", y="Campaign Name", orientation="h",
                      color="Budget Utilization (%)", color_continuous_scale="Blues", template="plotly_dark")
        fig3.update_layout(coloraxis_showscale=False, paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=10,b=0), height=420)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-title">CTR vs Conversion Rate</div>', unsafe_allow_html=True)
        fig4 = px.scatter(marketing_df, x="CTR (%)", y="Conv Rate (%)",
                          size="Conversions", color="Platform",
                          hover_name="Campaign Name",
                          color_discrete_sequence=COLORS, template="plotly_dark")
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            margin=dict(l=0,r=0,t=10,b=0), height=420, showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

    # ── FIX: .bar() instead of .background_gradient() — no matplotlib needed ──
    st.markdown('<div class="section-title">Campaign Performance Summary</div>', unsafe_allow_html=True)
    display_cols = ["Campaign Name","Platform","Budget","Spend","Impressions",
                    "Clicks","CTR (%)","Conversions","Conv Rate (%)","ROAS"]
    mkt_display = marketing_df[display_cols].copy()
    st.dataframe(
        mkt_display.style
                   .bar(subset=["ROAS"],          color="#10b981", vmin=0)
                   .bar(subset=["Conv Rate (%)"],  color="#6366f1", vmin=0)
                   .format({"ROAS":          lambda x: f"{x:.1f}" if pd.notnull(x) else "N/A",
                             "Budget":        "${:,.0f}",
                             "Spend":         "${:,.0f}",
                             "CTR (%)":       "{:.1f}%",
                             "Conv Rate (%)": "{:.0f}%"}),
        use_container_width=True
    )


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — GAP SUMMARY
# ════════════════════════════════════════════════════════════════════════════
elif tab_choice == "🔍 Gap Summary":
    st.title("🔍 Gap Analysis – Actionable Insights")

    st.markdown("### 🛍️ Fashion Gaps")
    col1, col2 = st.columns(2)
    with col1:
        st.error("**Low / Limited Stock Products**")
        gap_f = fashion_df[fashion_df["Status"].isin(["Low Stock","Limited Stock"])][
            ["Product Name","Category","Stock","Status"]]
        st.dataframe(gap_f, use_container_width=True)
    with col2:
        st.warning("**High Price, Low Stock (Revenue Risk)**")
        risk = fashion_df[(fashion_df["Price"] > 80) & (fashion_df["Stock"] < 100)][
            ["Product Name","Price","Stock","Rating"]]
        st.dataframe(risk, use_container_width=True)

    st.markdown("### 🎪 Event Management Gaps")
    col3, col4 = st.columns(2)
    with col3:
        st.error("**Underperforming Events (Fill Rate < 70%)**")
        low_fill = events_df[events_df["Fill Rate (%)"] < 70][
            ["Event Name","City","Capacity","Tickets Sold","Fill Rate (%)","Revenue"]
        ].sort_values("Fill Rate (%)")
        st.dataframe(low_fill, use_container_width=True)
    with col4:
        st.success("**High Revenue Events (Top Performers)**")
        top_events = events_df.nlargest(5, "Revenue")[
            ["Event Name","City","Tickets Sold","Revenue","Fill Rate (%)"]]
        st.dataframe(top_events, use_container_width=True)

    st.markdown("### 📣 Digital Marketing Gaps")
    col5, col6 = st.columns(2)
    mkt_clean = marketing_df.dropna(subset=["ROAS"])
    with col5:
        st.error("**Below-Target ROAS (< 4x)**")
        low_roas = mkt_clean[mkt_clean["ROAS"] < 4][
            ["Campaign Name","Platform","Spend","Conversions","ROAS"]]
        st.dataframe(low_roas, use_container_width=True)
    with col6:
        st.success("**Top Performing Campaigns (ROAS ≥ 8x)**")
        top_camp = mkt_clean[mkt_clean["ROAS"] >= 8][
            ["Campaign Name","Platform","Spend","Conversions","Conv Rate (%)","ROAS"]]
        st.dataframe(top_camp, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📋 Strategic Recommendations")
    recs = [
        ("🛍️ Fashion",   "Restock Ankle Strap Heels (60 units) and Ethnic Sherwani (40 units) — both high price, low availability = lost revenue."),
        ("🛍️ Fashion",   "Diamond Earrings (5.0 rating, $299.99) has only 30 units — premium item deserves better shelf depth."),
        ("🎪 Events",    "Indie Film Screening (79%), Photography Exhibition (70%), and Classical Dance Festival (70%) need targeted marketing pushes."),
        ("🎪 Events",    "Chennai & Pune events generate significantly lower revenue — local sponsorship or pricing strategy needed."),
        ("📣 Marketing", "Pause/reallocate budget from Brand Video – YouTube (ROAS 1.5x) and Twitter/X (1.8x) to top performers."),
        ("📣 Marketing", "Scale WhatsApp Broadcast (ROAS 9.8x) and Flash Sale pushes (ROAS 11.2x) — highest efficiency channels."),
        ("📣 Marketing", "Instagram Influencer Collab generated 2,250 conversions at $3K spend — increase influencer budget allocation."),
    ]
    for domain, rec in recs:
        st.markdown(f"- **{domain}**: {rec}")