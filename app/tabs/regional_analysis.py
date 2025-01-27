import streamlit as st
import pandas as pd
from app.utils.visualizations import (
    create_regional_bar_chart,
    create_line_chart,
    create_heatmap,
)


def render_regional_analysis(filtered_df):

    st.subheader("Sales Heatmap by Country and Category")
    heatmap_data = (
        filtered_df.groupby(["Country", "Category"])["Sales"].sum().reset_index()
    )
    heatmap_fig = create_heatmap(
        heatmap_data,
        x="Country",
        y="Category",
        values="Sales",
    )
    st.plotly_chart(heatmap_fig, use_container_width=True)
    analysis_type = st.selectbox(
        "Select Analysis Type",
        options=[
            "Region Sales",
            "Shipping Cost",
            "Regional Preferences",
            "Regional Profitability",
            "Regional Seasonality",
        ],
    )

    if analysis_type == "Region Sales":
        st.subheader("Region Sales Analysis")
        region_sales = filtered_df.groupby("Country")["Sales"].sum().reset_index()
        region_sales.columns = ["Country", "Total Sales"]

        if st.session_state["role"] == "admin":
            with st.expander("View Total Sales by Country"):
                st.dataframe(region_sales)

        st.plotly_chart(
            create_regional_bar_chart(
                region_sales,
                x="Country",
                y="Total Sales",
                title="Total Sales by Country",
                labels={"Country": "Country", "Total Sales": "Sales ($)"},
            ),
            use_container_width=True,
        )

    elif analysis_type == "Shipping Cost":
        st.subheader("Shipping Cost Analysis")
        shipping_costs = (
            filtered_df.groupby("Country")["Shipping.Cost"].mean().reset_index()
        )
        shipping_costs.columns = ["Country", "Average Shipping Cost"]

        if st.session_state["role"] == "admin":
            with st.expander("View Average Shipping Cost by Country"):
                st.dataframe(shipping_costs)

        st.plotly_chart(
            create_regional_bar_chart(
                shipping_costs,
                x="Country",
                y="Average Shipping Cost",
                title="Average Shipping Cost by Country",
                labels={"Country": "Country", "Average Shipping Cost": "Cost ($)"},
            ),
            use_container_width=True,
        )

    elif analysis_type == "Regional Preferences":
        st.subheader("Regional Preferences Analysis")
        regional_product_sales = (
            filtered_df.groupby(["Country", "Product.ID"])["Sales"].sum().reset_index()
        )
        regional_product_sales.columns = [
            "Country",
            "Product ID",
            "Regional Product Sales",
        ]

        if st.session_state["role"] == "admin":
            with st.expander("View Top-Selling Products by Country"):
                st.dataframe(regional_product_sales)

        st.plotly_chart(
            create_regional_bar_chart(
                regional_product_sales,
                x="Country",
                y="Regional Product Sales",
                color="Product ID",
                title="Top-Selling Products by Country",
                labels={"Country": "Country", "Regional Product Sales": "Sales ($)"},
                barmode="stack",
            ),
            use_container_width=True,
        )

    elif analysis_type == "Regional Profitability":
        st.subheader("Regional Profitability Analysis")
        region_profit = filtered_df.groupby("Country")["Profit"].sum().reset_index()
        region_profit.columns = ["Country", "Total Profit"]
        if st.session_state["role"] == "admin":
            with st.expander("View Total Profit by Country"):
                st.dataframe(region_profit)

        st.plotly_chart(
            create_regional_bar_chart(
                region_profit,
                x="Country",
                y="Total Profit",
                title="Total Profit by Country",
                labels={"Country": "Country", "Total Profit": "Profit ($)"},
            ),
            use_container_width=True,
        )

    elif analysis_type == "Regional Seasonality":
        st.subheader("Regional Seasonality Analysis")
        filtered_df["Month"] = pd.to_datetime(filtered_df["Order.Date"]).dt.month
        region_monthly_sales = (
            filtered_df.groupby(["Country", "Month"])["Sales"].sum().reset_index()
        )
        region_monthly_sales.columns = ["Country", "Month", "Monthly Sales"]

        if st.session_state["role"] == "admin":
            with st.expander("View Monthly Sales by Country"):
                st.dataframe(region_monthly_sales)

        st.plotly_chart(
            create_line_chart(
                region_monthly_sales,
                x="Month",
                y="Monthly Sales",
                color="Country",
                title="Monthly Sales by Country",
                labels={"Month": "Month", "Monthly Sales": "Sales ($)"},
            ),
            use_container_width=True,
        )
