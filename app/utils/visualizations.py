import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import pandas as pd


def create_bar_chart(data, x, y, title, labels, text=None):
    """
    Create a bar chart using Plotly.

    Parameters:
        data (pd.DataFrame): DataFrame containing data for the chart.
        x (str): Column name for the x-axis.
        y (str): Column name for the y-axis.
        title (str): Chart title.
        labels (dict): Labels for the axes.
        text (str, optional): Column name for displaying text values on bars.

    Returns:
        plotly.graph_objects.Figure: The bar chart.
    """
    fig = px.bar(
        data, x=x, y=y, title=title, labels=labels, text=text, template="plotly_white"
    )
    if text:
        fig.update_traces(texttemplate="$%{text:,.2f}", textposition="outside")
    fig.update_layout(title={"x": 0.5})
    return fig


def create_line_chart(data, x, y, title, labels, color=None, line_width=3):
    """
    Create a line chart using Plotly.

    Parameters:
        data (pd.DataFrame): DataFrame containing data for the chart.
        x (str): Column name for the x-axis.
        y (str): Column name for the y-axis.
        title (str): Chart title.
        labels (dict): Labels for the axes.
        color (str, optional): Column name for grouping by color.
        line_width (int): Width of the line.

    Returns:
        plotly.graph_objects.Figure: The line chart.
    """
    if color:
        fig = px.line(
            data,
            x=x,
            y=y,
            color=color,
            title=title,
            labels=labels,
            template="plotly_white",
        )
    else:
        fig = px.line(
            data, x=x, y=y, title=title, labels=labels, template="plotly_white"
        )

    fig.update_traces(line=dict(width=line_width))
    fig.update_layout(title={"x": 0.5})
    return fig


def create_regional_bar_chart(
    data, x, y, color=None, title=None, labels=None, barmode="group", text=None
):
    """
    Create a bar chart tailored for regional analysis using Plotly.

    Parameters:
        data (pd.DataFrame): DataFrame containing data for the chart.
        x (str): Column name for the x-axis.
        y (str): Column name for the y-axis.
        color (str, optional): Column name for grouping by color (e.g., "Region").
        title (str, optional): Chart title.
        labels (dict, optional): Labels for the axes.
        barmode (str, optional): Barmode for the chart (e.g., 'group', 'stack'). Defaults to 'group'.
        text (str, optional): Column name for displaying text values on bars.

    Returns:
        plotly.graph_objects.Figure: The regional bar chart.
    """
    fig = px.bar(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
        labels=labels,
        text=text,
        barmode=barmode,
        template="plotly_white",
    )
    if text:
        fig.update_traces(texttemplate="$%{text:,.2f}", textposition="outside")
    fig.update_layout(title={"x": 0.5})
    return fig


def create_pie_chart(data, names, title):
    """
    Create a pie chart using Plotly.

    Parameters:
        data (pd.DataFrame): DataFrame containing data for the chart.
        names (str): Column name for the pie chart labels.
        title (str): Title of the chart.

    Returns:
        plotly.graph_objects.Figure: The pie chart.
    """
    fig = px.pie(data, names=names, title=title, template="plotly_white")
    fig.update_layout(title={"x": 0.5})
    return fig


def create_scatter_plot(data, x, y, size, color, title, labels):
    """
    Create a scatter plot using Plotly.

    Parameters:
        data (pd.DataFrame): DataFrame containing data for the chart.
        x (str): Column name for the x-axis.
        y (str): Column name for the y-axis.
        size (str): Column name for the marker size.
        color (str): Column name for the marker color.
        title (str): Chart title.
        labels (dict): Labels for the axes.

    Returns:
        plotly.graph_objects.Figure: The scatter plot.
    """
    fig = px.scatter(
        data,
        x=x,
        y=y,
        size=size,
        color=color,
        title=title,
        labels=labels,
        template="plotly_white",
    )
    fig.update_layout(title={"x": 0.5})
    return fig


def create_histogram(data, x, title, labels):
    """
    Create a histogram using Plotly.

    Parameters:
        data (pd.DataFrame): DataFrame containing data for the histogram.
        x (str): Column name for the x-axis.
        title (str): Chart title.
        labels (dict): Labels for the axes.

    Returns:
        plotly.graph_objects.Figure: The histogram.
    """
    fig = px.histogram(data, x=x, title=title, labels=labels, template="plotly_white")
    fig.update_layout(title={"x": 0.5})
    return fig


def create_bar_chart_grouped(data, x, y, title, labels, barmode="group", color=None):
    """
    Create a grouped bar chart using Plotly.

    Parameters:
        data (pd.DataFrame): DataFrame containing data for the chart.
        x (str): Column name for the x-axis.
        y (list): List of column names for the y-axis.
        title (str): Chart title.
        labels (dict): Labels for the axes.
        barmode (str): Barmode for the chart (e.g., 'group', 'stack').
        color (str, optional): Column to color by.

    Returns:
        plotly.graph_objects.Figure: The grouped bar chart.
    """
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        labels=labels,
        barmode=barmode,
        color=color,
        template="plotly_white",
    )
    fig.update_layout(title={"x": 0.5})
    return fig


def create_choropleth_map(
    data, locations, locationmode, color, title, labels, color_scale="Blues"
):
    """
    Create a choropleth map using Plotly.

    Parameters:
        data (pd.DataFrame): DataFrame containing data for the map.
        locations (str): Column for country locations.
        locationmode (str): Location mode for the map (e.g., "country names").
        color (str): Column for the color scale.
        title (str): Map title.
        labels (dict): Labels for the axes.
        color_scale (str): Color scale for the map.

    Returns:
        plotly.graph_objects.Figure: The choropleth map.
    """
    fig = px.choropleth(
        data,
        locations=locations,
        locationmode=locationmode,
        color=color,
        title=title,
        labels=labels,
        template="plotly_white",
        color_continuous_scale=color_scale,
    )
    fig.update_layout(title={"x": 0.5})
    return fig


def create_forecast_plot(
    historical_data, forecast_data, x_col="ds", y_col="y", forecast_col="yhat"
):
    """
    Create a line chart for forecast visualization with historical data.

    Parameters:
        historical_data (pd.DataFrame): DataFrame containing historical sales data.
        forecast_data (pd.DataFrame): DataFrame containing forecasted sales data.
        x_col (str): Column for the x-axis (date).
        y_col (str): Column for historical sales data.
        forecast_col (str): Column for forecasted sales data.

    Returns:
        plotly.graph_objects.Figure: The forecast visualization.
    """
    fig = px.line(
        forecast_data,
        x=x_col,
        y=forecast_col,
        title="Sales Forecast",
        labels={x_col: "Date", forecast_col: "Forecasted Sales"},
        template="plotly_white",
    )
    fig.update_traces(line=dict(color="blue", width=3))

    fig.add_trace(
        go.Scatter(
            x=historical_data[x_col],
            y=historical_data[y_col],
            mode="markers+lines",
            name="Historical Sales",
        )
    )
    fig.update_layout(title={"x": 0.5}, xaxis_title="Date", yaxis_title="Sales ($)")
    return fig


def create_heatmap(data, x, y, values):
    """
    Create a heatmap using Plotly Express.

    Parameters:
        data (pd.DataFrame): The dataset.
        x (str): Column for the x-axis (e.g., 'Country').
        y (str): Column for the y-axis (e.g., 'Category').
        values (str): Column for the heatmap values (e.g., 'Sales').
        title (str): Title of the heatmap.
    """
    fig = px.imshow(
        data.pivot(index=y, columns=x, values=values),
        labels=dict(x=x, y=y, color=values),
        color_continuous_scale="Viridis",
    )
    fig.update_layout(xaxis_title=x, yaxis_title=y)
    return fig


def create_treemap(data, path, values):
    """
    Create a treemap using Plotly Express.

    Parameters:
        data (pd.DataFrame): The dataset.
        path (list): List of columns for hierarchical levels (e.g., ['Category', 'Sub-Category']).
        values (str): Column for the size of the treemap rectangles (e.g., 'Sales').
        title (str): Title of the treemap.
    """
    fig = px.treemap(
        data,
        path=path,
        values=values,
        color=values,
        color_continuous_scale="Blues",
    )
    return fig


def create_network_graph(data, source, target, title):
    """
    Create a network graph using Plotly and NetworkX.

    Parameters:
        data (pd.DataFrame): The dataset.
        source (str): Column for the source nodes (e.g., 'Customer.ID').
        target (str): Column for the target nodes (e.g., 'Product.ID').
        title (str): Title of the network graph.
    """
    # Create a graph from the data
    G = nx.from_pandas_edgelist(data, source=source, target=target)

    # Get positions for the nodes
    pos = nx.spring_layout(G)

    # Create edges
    edge_trace = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(
            go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                line=dict(width=0.5, color="#888"),
                hoverinfo="none",
                mode="lines",
            )
        )

    # Create nodes
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode="markers+text",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale="YlGnBu",
            size=10,
            colorbar=dict(thickness=15, title="Node Connections"),
        ),
    )

    for node in G.nodes():
        x, y = pos[node]
        node_trace["x"] += (x,)
        node_trace["y"] += (y,)
        node_trace["text"] += (node,)

    # Create the figure
    fig = go.Figure(
        data=edge_trace + [node_trace],
        layout=go.Layout(
            title=title,
            showlegend=False,
            hovermode="closest",
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
    )
    return fig
