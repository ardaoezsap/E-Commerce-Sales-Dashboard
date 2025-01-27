import bcrypt
import pandas as pd


def load_users(file_path="data/users.csv"):
    """
    Load user credentials from a CSV file.

    Parameters:
        file_path (str): Path to the users CSV file.

    Returns:
        pd.DataFrame: DataFrame containing user credentials.
    """
    return pd.read_csv(file_path)


def check_credentials(username, password, users_df):
    """
    Check if the provided username and password are valid.

    Parameters:
        username (str): The username provided by the user.
        password (str): The password provided by the user.
        users_df (pd.DataFrame): DataFrame containing user credentials.

    Returns:
        pd.Series or None: The user's data if the credentials are valid, otherwise None.
    """
    user = users_df[users_df["username"] == username]
    if not user.empty:
        hashed_password = user.iloc[0]["password"]
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
            return user.iloc[0]  # Return the user's data as a Series
    return None
