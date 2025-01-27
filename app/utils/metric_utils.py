def calculate_rfm(filtered_df, max_date):
    """
    Calculate RFM metrics for customer segmentation.

    Parameters:
        filtered_df (pd.DataFrame): Filtered DataFrame containing customer data.
        max_date (datetime): Maximum order date in the dataset.

    Returns:
        pd.DataFrame: DataFrame with RFM metrics and scores.
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


def calculate_repeat_purchase_rate(filtered_df):
    """
    Calculate repeat purchase rate.

    Parameters:
        filtered_df (pd.DataFrame): Filtered DataFrame containing customer data.

    Returns:
        float: Repeat purchase rate in percentage.
    """
    repeat_customers_data = filtered_df.groupby("Customer.Name").filter(
        lambda x: len(x) > 1
    )
    repeat_customers = repeat_customers_data["Customer.Name"].nunique()
    total_customers = filtered_df["Customer.Name"].nunique()
    return (repeat_customers / total_customers) * 100
