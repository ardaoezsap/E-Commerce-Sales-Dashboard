# Sales Analytics Dashboard

## Overview

The Sales Analytics Dashboard is a comprehensive Streamlit-based web application designed to provide insights into sales data, customer behavior, and product performance. The dashboard offers various analytical tools and visualizations to help businesses make data-driven decisions. It includes features such as sales forecasting, regional analysis, product performance tracking, customer insights, and order analysis.

## Features

### 1. **Sales Overview**
   - **Aggregated Sales Data**: View total sales, average sales per day, and total orders.
   - **Sales Over Time**: Visualize sales trends over time with interactive line charts.
   - **Sales by Product Category**: Analyze sales distribution across different product categories.
   - **Sales by Country**: Explore sales performance by country with bar charts and choropleth maps.

### 2. **Sales Forecasting**
   - **Forecast Future Sales**: Use the Prophet model to predict future sales trends.
   - **Customizable Forecast Period**: Adjust the forecast period (daily, weekly, monthly) and granularity.
   - **Forecast Visualization**: Compare historical sales data with forecasted sales using interactive line charts.

### 3. **Regional Analysis**
   - **Sales Heatmap**: Visualize sales distribution by country and category.
   - **Region Sales Analysis**: Analyze total sales by country.
   - **Shipping Cost Analysis**: Explore average shipping costs by country.
   - **Regional Preferences**: Identify top-selling products by country.
   - **Regional Profitability**: Analyze total profit by country.
   - **Regional Seasonality**: Examine monthly sales trends by country.

### 4. **Product Performance**
   - **Top-Selling Products**: Identify the best-selling products by sales.
   - **Sales Distribution by Category**: Visualize sales distribution across product categories and subcategories using treemaps.
   - **Most Profitable Products**: Analyze the most profitable products.
   - **Product Sales Trends**: Track sales trends for individual products over time.
   - **Seasonal Sales by Category**: Explore seasonal sales trends by product category.

### 5. **Order Analysis**
   - **Order Frequency Analysis**: Analyze the distribution of order frequency among customers.
   - **Average Order Value**: Calculate and visualize the average order value.
   - **Order Value Distribution**: Explore the distribution of order values.

### 6. **Customer Insights**
   - **Top Customers by Sales**: Identify the top customers based on total sales.
   - **Customer Lifetime Value (CLV)**: Analyze the lifetime value of customers.
   - **RFM Analysis**: Perform Recency, Frequency, and Monetary (RFM) analysis to segment customers.
   - **Customer Segmentation**: Visualize customer segments based on RFM scores.

### 7. **Login and User Management**
   - **Role-Based Access**: Differentiate between admin and regular users with role-based access control.
   - **Secure Login**: Implement secure login functionality with bcrypt password hashing.

## Installation

### Prerequisites

- Python 3.8 or higher
- Streamlit
- Pandas
- Plotly
- Prophet
- Bcrypt

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/sales-analytics-dashboard.git
   cd sales-analytics-dashboard
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run app/dashboard.py
   ```

4. **Access the Dashboard**:
   Open your web browser and navigate to `http://localhost:8501`.

### Example Login Data
- **User**:  
  - Username: `user1`  
  - Password: `password1`  

- **Admin**:  
  - Username: `admin`  
  - Password: `admin123`  

---

## Usage

1. **Login**: Use the provided credentials to log in. Admins have access to additional data and settings.
2. **Navigate Tabs**: Use the sidebar to navigate between different analytical tabs.
3. **Filter Data**: Apply filters to focus on specific time periods, regions, or products.
4. **View Visualizations**: Explore interactive charts and graphs to gain insights into sales and customer behavior.
5. **Export Data**: Admins can export filtered and aggregated data for further analysis.

## Project Structure

```
sales-analytics-dashboard/
├── app/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── customer_insights.py
│   ├── login_tab.py
│   ├── order_analysis.py
│   ├── product_performance.py
│   ├── regional_analysis.py
│   ├── sales_forecasting_tab.py
│   ├── sales_overview.py
│   └── utils/
│       ├── __init__.py
│       ├── data_processing.py
│       └── visualizations.py
├── data/
│   ├── customers.csv
│   ├── merged_data.csv
│   ├── orders.csv
│   ├── products.csv
│   ├── sales.csv
│   └── users.csv
├── scripts/
│   └── forecasting/
│       ├── __init__.py
│       └── sales_forecasting.py
├── Procfile
├── README.md
└── requirements.txt
```


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Streamlit**: For providing an excellent framework for building data apps.
- **Prophet**: For the robust forecasting model.
- **Plotly**: For interactive and beautiful visualizations.

## Contact

For any questions or suggestions, please contact Arda Özsap at ardaozsap03@gmail.com.

---

**Happy Analyzing!** 🚀