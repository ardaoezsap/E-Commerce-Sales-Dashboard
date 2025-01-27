import streamlit as st
from ..utils.data_processing import aggregate_sales_by_column
from app.utils.visualizations import (
    create_line_chart,
    create_bar_chart,
    create_choropleth_map,
)


def render_sales_overview(filtered_df):

    if st.session_state["role"] == "admin":
        with st.expander("View Filtered Data"):
            st.dataframe(filtered_df)

    sales_over_time = aggregate_sales_by_column(
        filtered_df, group_by="Order.Date", value_column="Sales"
    )
    sales_over_time.rename(
        columns={"Order.Date": "Date", "Sales": "Total Sales"}, inplace=True
    )

    if sales_over_time.empty:
        st.error("No sales data available for the selected filters.")
        return

    if st.session_state["role"] == "admin":
        with st.expander("Aggregated Sales Data"):
            st.dataframe(sales_over_time)

    total_sales = sales_over_time["Total Sales"].sum()
    avg_sales = sales_over_time["Total Sales"].mean()
    total_orders = len(filtered_df)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", f"${total_sales:,.2f}")
    with col2:
        st.metric("Average Sales (per Day)", f"${avg_sales:,.2f}")
    with col3:
        st.metric("Total Orders", total_orders)

    if (sales_over_time["Total Sales"] == 0).any():
        st.warning("Sales are 0 for one or more days in the selected date range.")

    if sales_over_time["Date"].nunique() > 1:
        st.plotly_chart(
            create_line_chart(
                sales_over_time,
                x="Date",
                y="Total Sales",
                title="Sales Over Time",
                labels={"Date": "Order Date", "Total Sales": "Sales ($)"},
            ),
            use_container_width=True,
        )
    else:
        st.info(
            "All sales occur on the same date. Cannot plot a meaningful Sales Over Time graph."
        )

    if "Category" in filtered_df.columns:
        category_sales = aggregate_sales_by_column(
            filtered_df, group_by="Category", value_column="Sales"
        )
        category_sales.rename(columns={"Sales": "Total Sales"}, inplace=True)

        st.plotly_chart(
            create_bar_chart(
                category_sales,
                x="Category",
                y="Total Sales",
                title="Sales by Product Category",
                labels={"Category": "Product Category", "Total Sales": "Sales ($)"},
                text="Total Sales",
            ),
            use_container_width=True,
        )

    if "Country" in filtered_df.columns:
        country_sales = aggregate_sales_by_column(
            filtered_df, group_by="Country", value_column="Sales"
        )
        country_sales.rename(columns={"Sales": "Total Sales"}, inplace=True)

        st.plotly_chart(
            create_bar_chart(
                country_sales,
                x="Country",
                y="Total Sales",
                title="Sales by Country",
                labels={"Country": "Country", "Total Sales": "Sales ($)"},
                text="Total Sales",
            ),
            use_container_width=True,
        )

        st.plotly_chart(
            create_choropleth_map(
                country_sales,
                locations="Country",
                locationmode="country names",
                color="Total Sales",
                title="Sales Distribution Across Countries",
                labels={"Country": "Country", "Total Sales": "Sales ($)"},
            ),
            use_container_width=True,
        )
    else:
        st.warning("The 'Country' column is missing in the dataset.")
