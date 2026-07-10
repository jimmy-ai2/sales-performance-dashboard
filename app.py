import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Sales Performance Dashboard", page_icon="📊", layout="wide"
)


# 2. Mock Data Generation
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", end="2026-06-30", freq="D")
    products = ["Electronics", "Clothing", "Home & Kitchen", "Books"]
    regions = ["North", "South", "East", "West"]

    data = {
        "Date": np.random.choice(dates, size=500),
        "Product_Category": np.random.choice(products, size=500),
        "Region": np.random.choice(regions, size=500),
        "Sales": np.random.uniform(20, 500, size=500).round(2),
        "Units_Sold": np.random.randint(1, 10, size=500),
    }
    df = pd.DataFrame(data)
    df["Profit"] = (df["Sales"] * np.random.uniform(0.15, 0.4, size=500)).round(2)
    return df.sort_values("Date")


df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filter Options")

# Region Filter
all_regions = ["All"] + list(df["Region"].unique())
selected_region = st.sidebar.selectbox("Select Region", all_regions)

# Product Filter
all_products = ["All"] + list(df["Product_Category"].unique())
selected_product = st.sidebar.selectbox("Select Product Category", all_products)

# Filter Logic
filtered_df = df.copy()
if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]
if selected_product != "All":
    filtered_df = filtered_df[filtered_df["Product_Category"] == selected_product]

# 4. Main Dashboard UI
st.title("📊 Sales Performance Dashboard")
st.markdown("Real-time business metrics and performance tracking.")
st.markdown("---")

# KPI Metrics Row
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_units = filtered_df["Units_Sold"].sum()
margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric(label="Total Sales", value=f"${total_sales:,.2f}")
kpi2.metric(label="Total Profit", value=f"${total_profit:,.2f}")
kpi3.metric(label="Units Sold", value=f"{total_units:,}")
kpi4.metric(label="Profit Margin", value=f"{margin:.1f}%")

st.markdown("---")

# Charts Row
chart1, chart2 = st.columns(2)

with chart1:
    st.subheader("Sales Trend Over Time")
    daily_sales = filtered_df.groupby("Date")["Sales"].sum().reset_index()
    fig_line = px.line(daily_sales, x="Date", y="Sales", template="plotly_white")
    st.plotly_chart(fig_line, use_container_width=True)

with chart2:
    st.subheader("Sales by Product Category")
    prod_sales = filtered_df.groupby("Product_Category")["Sales"].sum().reset_index()
    fig_bar = px.bar(
        prod_sales,
        x="Product_Category",
        y="Sales",
        color="Product_Category",
        template="plotly_white",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# Data Table Row
st.subheader("Filtered Transaction Data")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
