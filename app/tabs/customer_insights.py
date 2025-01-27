import pandas as pd
import streamlit as st
from app.utils.visualizations import (
    create_pie_chart,
    create_bar_chart,
    create_scatter_plot,
)


def render_customer_insights(filtered_df):
    filtered_df["Order.Date"] = pd.to_datetime(filtered_df["Order.Date"])
    max_date = filtered_df["Order.Date"].max()

    st.subheader("Top Customers by Sales")
    customer_sales = (
        filtered_df.groupby("Customer.Name")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
        .head(10)
    )

    if st.session_state["role"] == "admin":
        with st.expander("View Top Customers by Sales"):
            st.dataframe(customer_sales)

    st.plotly_chart(
        create_bar_chart(
            customer_sales,
            x="Customer.Name",
            y="Sales",
            title="Top Customers by Sales",
            labels={"Customer.Name": "Customer Name", "Sales": "Sales ($)"},
        ),
        use_container_width=True,
    )

    st.subheader("Customer Lifetime Value (CLV)")
    customer_clv = (
        filtered_df.groupby("Customer.Name")["Sales"]
        .sum()
        .reset_index()
        .rename(columns={"Sales": "CLV"})
        .sort_values("CLV", ascending=False)
        .head(10)
    )

    if st.session_state["role"] == "admin":
        with st.expander("View Customer Lifetime Value"):
            st.dataframe(customer_clv)

    st.plotly_chart(
        create_bar_chart(
            customer_clv,
            x="Customer.Name",
            y="CLV",
            title="Top Customers by Lifetime Value",
            labels={"Customer.Name": "Customer Name", "CLV": "Lifetime Value ($)"},
        ),
        use_container_width=True,
    )

    st.subheader("RFM Analysis")
    rfm = (
        filtered_df.groupby("Customer.Name")
        .agg(
            Recency=("Order.Date", lambda x: (max_date - x.max()).days),
            Frequency=("Order.ID", "count"),
            Monetary=("Sales", "sum"),
        )
        .reset_index()
    )

    rfm["RFM_Score"] = rfm["Recency"] + rfm["Frequency"] + rfm["Monetary"]
    rfm["RFM_Score_rank"] = rfm["RFM_Score"].rank(method="first")

    try:
        rfm["Segment"] = pd.qcut(
            rfm["RFM_Score_rank"],
            q=4,
            labels=["Low-Value", "Mid-Value", "High-Value", "Top-Value"],
        )
    except ValueError:
        rfm["Segment"] = "Single Segment"

    if st.session_state["role"] == "admin":
        with st.expander("View RFM Metrics"):
            st.dataframe(rfm.head(10))

    st.plotly_chart(
        create_scatter_plot(
            rfm,
            x="Recency",
            y="Frequency",
            size="Monetary",
            color="Monetary",
            title="RFM Analysis: Recency vs Frequency",
            labels={
                "Recency": "Recency (Days)",
                "Frequency": "Frequency",
                "Monetary": "Monetary Value ($)",
            },
        ),
        use_container_width=True,
    )

    st.subheader("Customer Segmentation")

    if st.session_state["role"] == "admin":
        with st.expander("View Customer Segments"):
            st.dataframe(rfm[["Customer.Name", "Segment"]].head(10))

    st.plotly_chart(
        create_pie_chart(
            rfm,
            names="Segment",
            title="Customer Segmentation by RFM Score",
        ),
        use_container_width=True,
    )
