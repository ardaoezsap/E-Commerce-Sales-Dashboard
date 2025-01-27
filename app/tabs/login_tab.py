import streamlit as st
import pandas as pd
from app.utils.auth_utils import check_credentials


def load_users():
    return pd.read_csv("data/users.csv")


def render_login_tab():

    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    users_df = load_users()

    if st.button("Login"):
        user = check_credentials(username, password, users_df)
        if user is not None:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["name"] = user["name"]
            st.session_state["surname"] = user["surname"]
            st.session_state["role"] = user["role"]

            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid username or password")
