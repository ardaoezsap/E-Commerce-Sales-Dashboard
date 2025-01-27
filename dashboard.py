# Copyright (c) 2025 Arda Özsap
# Licensed under the MIT License (see LICENSE for details)

from pathlib import Path
import sys
import pandas as pd
import streamlit as st
from app.tabs.sales_overview import render_sales_overview
from app.tabs.product_performance import render_product_performance
from app.tabs.customer_insights import render_customer_insights
from app.tabs.sales_forecasting_tab import render_sales_forecasting
from app.tabs.regional_analysis import render_regional_analysis
from app.tabs.login_tab import render_login_tab
from app.tabs.order_analysis import render_order_analysis
from app.chatbot.chatbot import ask_question


root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))


def initialize_session_state(defaults):
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_and_prepare_data(file_path):
    data = pd.read_csv(file_path)
    data["Order.Date"] = pd.to_datetime(data["Order.Date"]).dt.date
    return data


def render_sidebar_profile():
    with st.sidebar.expander("🔑 Profile", expanded=False):
        st.write(f"**Name**: {st.session_state['name']}")
        st.write(f"**Surname**: {st.session_state['surname']}")
        st.write(f"**Role**: {st.session_state['role']}")


def render_sidebar_filters_and_chatbot():
    with st.sidebar.expander("🔍 Filters", expanded=True):
        chat_input = st.text_input("Enter your message here:")
        send_button = st.button("Send")

        if send_button and chat_input:
            process_chatbot_input(ask_question(chat_input))

        render_manual_filters()


def process_chatbot_input(data):
    if data.country:
        st.session_state.country_filter = [
            c for c in data.country if c in merged_df["Country"].unique()
        ]
    else:
        st.session_state.country_filter = []

    if data.product_category:
        st.session_state.category_filter = [
            cat
            for cat in data.product_category
            if cat in merged_df["Category"].unique()
        ]
    else:
        st.session_state.category_filter = []

    if data.start_date and data.end_date:
        st.session_state.date_range = [data.start_date, data.end_date]
    elif data.start_date:
        st.session_state.date_range = [data.start_date, dataset_max_date]

    if data.tab:
        st.session_state["active_tab"] = data.tab

    st.session_state.trigger_rerun = True
    st.rerun()


def render_manual_filters():
    valid_country_defaults = [
        c for c in st.session_state.country_filter if c in merged_df["Country"].unique()
    ]
    country_filter = st.multiselect(
        "Select Country",
        merged_df["Country"].unique(),
        default=valid_country_defaults,
    )
    st.session_state.country_filter = country_filter

    valid_category_defaults = [
        cat
        for cat in st.session_state.category_filter
        if cat in merged_df["Category"].unique()
    ]
    category_filter = st.multiselect(
        "Select Product Category",
        merged_df["Category"].unique(),
        default=valid_category_defaults,
    )
    st.session_state.category_filter = category_filter

    if not st.session_state.date_range:
        st.session_state.date_range = [dataset_min_date, dataset_max_date]

    date_range_input = st.date_input(
        "Select Date Range",
        value=(st.session_state.date_range[0], st.session_state.date_range[1]),
    )
    if len(date_range_input) == 2:
        st.session_state.date_range = list(date_range_input)


def filter_data(data):
    start_date, end_date = st.session_state.date_range

    if start_date == end_date:
        st.warning("Start date and end date cannot be the same.")
        st.stop()

    filtered = data.loc[
        (
            data["Country"].isin(st.session_state.country_filter)
            if st.session_state.country_filter
            else True
        )
        & (
            data["Category"].isin(st.session_state.category_filter)
            if st.session_state.category_filter
            else True
        )
        & (data["Order.Date"] >= start_date)
        & (data["Order.Date"] <= end_date)
    ]
    return filtered


def render_tabs(filtered_df):
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Sales Overview",
            "Product Performance",
            "Customer Insights",
            "Sales Forecasting",
            "Regional Analysis",
            "Order Analysis",
        ]
    )

    with tab1:
        render_sales_overview(filtered_df)

    with tab2:
        render_product_performance(filtered_df)

    with tab3:
        render_customer_insights(filtered_df)

    with tab4:
        render_sales_forecasting(filtered_df)

    with tab5:
        render_regional_analysis(filtered_df)

    with tab6:
        render_order_analysis(filtered_df)


def render_logout_button():
    """
    Renders a Logout button at the bottom of the sidebar.
    """
    st.sidebar.write("---")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()


if __name__ == "__main__":
    session_state_defaults = {
        "logged_in": False,
        "username": "jdoe",
        "name": "John",
        "surname": "Doe",
        "role": "Analyst",
        "country_filter": [],
        "category_filter": [],
        "date_range": [],
        "trigger_rerun": False,
    }
    initialize_session_state(session_state_defaults)

    merged_df = load_and_prepare_data("data/merged_data.csv")
    dataset_min_date = merged_df["Order.Date"].min()
    dataset_max_date = merged_df["Order.Date"].max()

    st.title("E-Commerce Sales Dashboard")

    if not st.session_state["logged_in"]:
        render_login_tab()
    else:
        render_sidebar_profile()
        render_sidebar_filters_and_chatbot()
        render_logout_button()
        filtered_df = filter_data(merged_df)
        if filtered_df.empty:
            st.warning("No data found for the selected filters.")
        else:
            render_tabs(filtered_df)
