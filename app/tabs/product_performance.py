import streamlit as st
from app.utils.data_processing import calculate_top_values, add_season_column
from app.utils.visualizations import create_bar_chart_grouped, create_treemap
import plotly.express as px


def render_product_performance(filtered_df):
    if "Product Name" in filtered_df.columns:
        st.subheader("Top-Selling Products by Sales")
        product_sales = calculate_top_values(
            filtered_df, group_by="Product Name", value_column="Sales", sort_by="Sales"
        )

        if st.session_state["role"] == "admin":
            with st.expander("View Top-Selling Products Data"):
                st.dataframe(product_sales)

        st.plotly_chart(
            create_bar_chart_grouped(
                product_sales,
                x="Product Name",
                y=["Sales"],
                title="Top-Selling Products by Sales",
                labels={"Product Name": "Product", "Sales": "Sales ($)"},
            )
        )
        st.subheader("Sales Distribution by Product Category and Subcategory")
        treemap_data = (
            filtered_df.groupby(["Category", "Sub-Category"])["Sales"]
            .sum()
            .reset_index()
        )
        treemap_fig = create_treemap(
            treemap_data,
            path=["Category", "Sub-Category"],
            values="Sales",
        )
        st.plotly_chart(treemap_fig, use_container_width=True)
        st.subheader("Most Profitable Products")
        product_profit = calculate_top_values(
            filtered_df,
            group_by="Product Name",
            value_column="Profit",
            sort_by="Profit",
        )

        if st.session_state["role"] == "admin":
            with st.expander("View Product Profitability Data"):
                st.dataframe(product_profit)

        st.plotly_chart(
            create_bar_chart_grouped(
                product_profit,
                x="Product Name",
                y=["Profit"],
                title="Most Profitable Products",
                labels={"Product Name": "Product", "Profit": "Profit ($)"},
            )
        )

        st.subheader("Product Sales Trends Over Time")
        selected_product = st.selectbox(
            "Select a Product", filtered_df["Product Name"].unique()
        )
        product_trend = (
            filtered_df[filtered_df["Product Name"] == selected_product]
            .groupby("Order.Date")["Sales"]
            .sum()
            .reset_index()
        )

        st.plotly_chart(
            create_bar_chart_grouped(
                product_trend,
                x="Order.Date",
                y=["Sales"],
                title=f"Sales Trends for {selected_product}",
                labels={"Order.Date": "Date", "Sales": "Sales ($)"},
            )
        )

        if "Category" in filtered_df.columns and "Country" in filtered_df.columns:
            st.subheader("Most Sold Product Category by Country")

            country_category_sales = (
                filtered_df.groupby(["Country", "Category"])["Sales"]
                .sum()
                .reset_index()
            )

            most_sold_category_by_country = country_category_sales.loc[
                country_category_sales.groupby("Country")["Sales"].idxmax()
            ]

            if st.session_state["role"] == "admin":
                with st.expander("View Most Sold Categories by Country"):
                    st.dataframe(most_sold_category_by_country)

            fig = px.choropleth(
                most_sold_category_by_country,
                locations="Country",
                locationmode="country names",
                color="Category",
                title="Most Sold Product Category by Country",
                labels={"Category": "Product Category"},
                color_discrete_sequence=px.colors.qualitative.Plotly,
                template="plotly_white",
            )
            fig.update_layout(title={"x": 0.5})
            st.plotly_chart(fig, use_container_width=True)

        if "Category" in filtered_df.columns:
            st.subheader("Seasonal Sales by Category")
            filtered_df = add_season_column(filtered_df, date_column="Order.Date")
            seasonal_sales = (
                filtered_df.groupby(["Season", "Category"])["Sales"].sum().reset_index()
            )

            if st.session_state["role"] == "admin":
                with st.expander("View Seasonal Sales by Category"):
                    st.dataframe(seasonal_sales)

            st.plotly_chart(
                create_bar_chart_grouped(
                    seasonal_sales,
                    x="Season",
                    y=["Sales"],
                    title="Seasonal Sales by Category",
                    labels={
                        "Season": "Season",
                        "Sales": "Total Sales ($)",
                        "Category": "Product Category",
                    },
                    color="Category",
                )
            )

        else:
            st.warning("The 'Category' column is missing in the dataset.")
    else:
        st.warning("The 'Product Name' column is missing in the dataset.")
