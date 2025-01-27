import pandas as pd


def calculate_rfm(filtered_df, max_date):
    """
    Calculate RFM metrics for customer segmentation.

    Parameters:
        filtered_df (pd.DataFrame): Filtered DataFrame containing customer data.
        max_date (datetime): Maximum order date in the dataset.

    Returns:
        pd.DataFrame: DataFrame with RFM metrics (Recency, Frequency, Monetary).
    """
    rfm = (
        filtered_df.groupby("Customer.Name")
        .agg(
            Recency=("Order.Date", lambda x: (max_date - x.max()).days),
            Frequency=("Order.ID", "count"),
            Monetary=("Sales", "sum"),
        )
        .reset_index()
    )
    return rfm


def calculate_order_frequency(filtered_df):
    """
    Calculate the frequency of orders for each customer.

    Parameters:
        filtered_df (pd.DataFrame): The filtered DataFrame containing order data.

    Returns:
        pd.DataFrame: DataFrame with columns 'Customer ID' and 'Order Count'.
    """
    order_frequency = (
        filtered_df.groupby("Customer.ID")["Order.ID"].count().reset_index()
    )
    order_frequency.columns = ["Customer ID", "Order Count"]
    return order_frequency


def calculate_order_value(filtered_df):
    """
    Calculate the value of each order.

    Parameters:
        filtered_df (pd.DataFrame): The filtered DataFrame containing sales data.

    Returns:
        pd.DataFrame: DataFrame with columns 'Order ID' and 'Order Value'.
    """
    order_value = filtered_df.groupby("Order.ID")["Sales"].sum().reset_index()
    order_value.columns = ["Order ID", "Order Value"]
    return order_value


def calculate_top_values(filtered_df, group_by, value_column, sort_by, top_n=10):
    """
    Calculate the top values for a specific group.

    Parameters:
        filtered_df (pd.DataFrame): Filtered DataFrame containing data.
        group_by (str): Column to group by.
        value_column (str): Column to calculate the sum for.
        sort_by (str): Column to sort by.
        top_n (int): Number of top rows to return.

    Returns:
        pd.DataFrame: DataFrame with top values.
    """
    grouped_data = (
        filtered_df.groupby(group_by)[value_column]
        .sum()
        .reset_index()
        .sort_values(sort_by, ascending=False)
        .head(top_n)
    )
    return grouped_data


def add_season_column(filtered_df, date_column):
    """
    Add a season column based on a date column.

    Parameters:
        filtered_df (pd.DataFrame): Filtered DataFrame containing a date column.
        date_column (str): Name of the date column.

    Returns:
        pd.DataFrame: DataFrame with an additional season column.
    """

    def get_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        elif month in [9, 10, 11]:
            return "Fall"

    filtered_df["Month"] = pd.to_datetime(filtered_df[date_column]).dt.month
    filtered_df["Season"] = filtered_df["Month"].apply(get_season)
    return filtered_df


def calculate_aggregated_values(filtered_df, group_by, value_column, agg_func="sum"):
    """
    Calculate aggregated values for a specific column grouped by another column.

    Parameters:
        filtered_df (pd.DataFrame): The filtered DataFrame containing data.
        group_by (list): List of columns to group by.
        value_column (str): Column to aggregate.
        agg_func (str): Aggregation function (default is "sum").

    Returns:
        pd.DataFrame: DataFrame with aggregated values.
    """
    aggregated_data = (
        filtered_df.groupby(group_by)[value_column].agg(agg_func).reset_index()
    )
    return aggregated_data


def add_month_column(filtered_df, date_column):
    """
    Add a month column based on a date column.

    Parameters:
        filtered_df (pd.DataFrame): Filtered DataFrame containing a date column.
        date_column (str): Name of the date column.

    Returns:
        pd.DataFrame: DataFrame with an additional month column.
    """
    filtered_df["Month"] = pd.to_datetime(filtered_df[date_column]).dt.month
    return filtered_df


def preprocess_sales_data(data, date_column, sales_column, granularity="Daily"):
    """
    Preprocess sales data for Prophet model with selected granularity.

    Parameters:
        data (pd.DataFrame): The dataset containing historical sales data.
        date_column (str): Column name for the order date.
        sales_column (str): Column name for sales data.
        granularity (str): Granularity for aggregation ('Daily', 'Weekly', 'Monthly').

    Returns:
        pd.DataFrame: Aggregated sales data with columns "ds" (date) and "y" (sales).
    """
    data[date_column] = pd.to_datetime(data[date_column])

    sales_over_time = data.groupby(date_column)[sales_column].sum().reset_index()
    sales_over_time.columns = ["ds", "y"]

    if granularity == "Weekly":
        sales_over_time["ds"] = (
            sales_over_time["ds"].dt.to_period("W").apply(lambda r: r.start_time)
        )
    elif granularity == "Monthly":
        sales_over_time["ds"] = (
            sales_over_time["ds"].dt.to_period("M").apply(lambda r: r.start_time)
        )

    sales_over_time = sales_over_time.groupby("ds")["y"].sum().reset_index()
    return sales_over_time


def calculate_forecast(data, periods=30, freq="D"):
    """
    Forecast future sales using the Prophet model.

    Parameters:
        data (pd.DataFrame): The dataset containing historical sales data.
        periods (int): Number of future periods to forecast.
        freq (str): Frequency for future dates ('D' for daily, 'W' for weekly, etc.).

    Returns:
        pd.DataFrame: A DataFrame with the forecasted sales.
    """
    from prophet import Prophet

    model = Prophet()
    model.fit(data)

    future = model.make_future_dataframe(periods=periods, freq=freq)
    forecast = model.predict(future)

    return forecast[["ds", "yhat"]].tail(periods)


def aggregate_sales_by_column(filtered_df, group_by, value_column):
    """
    Aggregate sales data by a specific column.

    Parameters:
        filtered_df (pd.DataFrame): The filtered DataFrame containing sales data.
        group_by (str): Column to group by.
        value_column (str): Column containing sales data.

    Returns:
        pd.DataFrame: Aggregated sales data.
    """
    aggregated_data = filtered_df.groupby(group_by, as_index=False)[value_column].sum()
    return aggregated_data
