import streamlit as st
from app.utils.data_processing import preprocess_sales_data
import plotly.express as px
import plotly.graph_objects as go

from scripts.forecasting.sales_forecasting import forecast_sales_prophet


def render_sales_forecasting(filtered_df):
    st.markdown(
        "Use advanced forecasting models to predict future sales trends and uncover potential growth opportunities."
    )

    if len(filtered_df) < 2:
        st.warning(
            "Not enough data for forecasting. At least 2 rows of data are required."
        )
        return

    try:
        st.subheader("Forecast Settings")
        periods = st.slider(
            "Select Forecast Period (days)", min_value=7, max_value=90, value=30
        )
        granularity = st.radio(
            "Select Granularity for Forecast", ["Daily", "Weekly", "Monthly"], index=0
        )

        date_column = "Order.Date"
        sales_column = "Sales"

        preprocessed_data = preprocess_sales_data(
            filtered_df,
            date_column=date_column,
            sales_column=sales_column,
            granularity=granularity,
        )

        forecast_df = forecast_sales_prophet(preprocessed_data, periods)

        st.subheader("Forecast Summary")
        st.metric("Total Forecasted Sales", f"${forecast_df['yhat'].sum():,.2f}")
        st.metric("Average Sales per Day", f"${forecast_df['yhat'].mean():,.2f}")

        if st.session_state["role"] == "admin":
            with st.expander("View Forecasted Data"):
                st.dataframe(forecast_df)

        st.subheader("Sales Forecast Visualization")
        fig = px.line(
            forecast_df,
            x="ds",
            y="yhat",
            title=f"Sales Forecast ({granularity})",
            labels={"ds": "Date", "yhat": "Forecasted Sales"},
            template="plotly_white",
        )
        fig.update_traces(line=dict(color="blue", width=3))
        fig.add_trace(
            go.Scatter(
                x=preprocessed_data["ds"],
                y=preprocessed_data["y"],
                mode="markers+lines",
                name="Historical Sales",
            )
        )
        fig.update_layout(title={"x": 0.5}, xaxis_title="Date", yaxis_title="Sales ($)")
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred during forecasting: {str(e)}")
