import streamlit as st
from app.utils.visualizations import create_histogram


def render_order_analysis(filtered_df):

    st.subheader("Order Frequency Analysis")
    order_frequency = (
        filtered_df.groupby("Customer.ID")["Order.ID"].count().reset_index()
    )
    order_frequency.columns = ["Customer ID", "Order Count"]

    if st.session_state["role"] == "admin":
        with st.expander("View Order Frequency Data"):
            st.dataframe(order_frequency)

    st.plotly_chart(
        create_histogram(
            order_frequency,
            x="Order Count",
            title="Distribution of Order Frequency",
            labels={"Order Count": "Number of Orders", "count": "Number of Customers"},
        )
    )

    st.subheader("Average Order Value Analysis")
    order_value = filtered_df.groupby("Order.ID")["Sales"].sum().reset_index()
    order_value.columns = ["Order ID", "Order Value"]

    if st.session_state["role"] == "admin":
        with st.expander("View Order Value Data"):
            st.dataframe(order_value)

    avg_order_value = order_value["Order Value"].mean()
    st.metric("Average Order Value", f"${avg_order_value:,.2f}")

    st.plotly_chart(
        create_histogram(
            order_value,
            x="Order Value",
            title="Distribution of Order Values",
            labels={
                "Order Value": "Order Value ($)",
                "count": "Number of Orders",
            },
        )
    )
