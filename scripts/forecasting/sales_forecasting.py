from prophet import Prophet


def forecast_sales_prophet(data, periods=30):
    """
    Forecast future sales using the Prophet model.

    Parameters:
        data (pd.DataFrame): The dataset containing historical sales data.
        periods (int): Number of future periods to forecast.

    Returns:
        pd.DataFrame: A DataFrame with the forecasted sales.
    """
    model = Prophet()
    model.fit(data)

    freq = "D"
    if periods == "Weekly":
        freq = "W"
    elif periods == "Monthly":
        freq = "M"

    future = model.make_future_dataframe(periods=periods, freq=freq)
    forecast = model.predict(future)

    return forecast[["ds", "yhat"]].tail(periods)
