"""
Category Analysis Dash Application
==================================

This Dash application provides an analysis of Google Play Store app data,
allowing users to filter and visualize statistics by app type (Free or Paid)
and examine category-wise distributions of apps, ratings, and prices.

The application is built with Dash and Plotly and includes the following features:
- Total Apps count, Average Rating, and Free Apps percentage displayed dynamically.
- Interactive visualizations for category distributions, ratings, and prices.

Modules and Dependencies
------------------------
- `os`: File system operations.
- `pandas`: Data manipulation and analysis.
- `dash`: Core framework for creating Dash apps.
- `dash_bootstrap_components`: Bootstrap styling components for Dash.
- `plotly.express`: Simplified interface for Plotly visualizations.
- `numpy`: Numerical operations and array manipulations.
- `playstore.config`: Configuration for the application.

"""

import os
import pandas as pd
from dash import html, dcc, callback, Output, Input, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np
from playstore.config import CLEAN_DATA_DIR

# Page Registration
register_page(__name__, path="/category-analysis", name="Category Analysis")

# Load Data
try:
    df = pd.read_csv(os.path.join(CLEAN_DATA_DIR, "cleaned_googleplaystore.csv"))
except Exception:
    df = pd.DataFrame({
        'Category': ['Game', 'Education', 'Business'],
        'Rating': [4.5, 4.0, 3.8],
        'Type': ['Free', 'Free', 'Paid'],
        'Installs': [1000000, 500000, 100000],
    })

layout = html.Div(
    [
        html.H1("Category Analysis", className="text-google-play text-center mb-4"),
        html.Div([
            dcc.RadioItems(
                id='app-type-filter',
                options=[
                    {'label': ' All', 'value': 'all'},
                    {'label': ' Free', 'value': 'Free'},
                    {'label': ' Paid', 'value': 'Paid'}
                ],
                value='all',
                className="form-check-inline"
            )
        ], className="card p-4 shadow-sm mb-4"),

        html.Div([
            html.Div([
                html.H3("Total Apps", className="h5 text-muted"),
                html.P(id='total-apps', className="display-6 text-primary fw-bold")
            ], className="card p-2 shadow-sm col-md-3 m-2"),
            html.Div([
                html.H3("Average Rating", className="h5 text-muted"),
                html.P(id='avg-rating', className="display-6 text-success fw-bold")
            ], className="card p-2 shadow-sm col-md-3 m-2"),
            html.Div([
                html.H3("Free Apps", className="h5 text-muted"),
                html.P(id='free-apps-pct', className="display-6 text-info fw-bold")
            ], className="card p-2 shadow-sm col-md-3 m-2")
        ], className="row justify-content-center mb-4"),

        html.Div([
            dcc.Graph(id="category-distribution"),
            dcc.Graph(id="rating-distribution"),
            dcc.Graph(id="content-rating-boxplot"),
            dcc.Graph(id="average-price-category"),
        ], className="mb-4")
    ],
    className="container",
)
# Layout Definition

# Callbacks for Dynamic Updates
@callback(
    [Output('total-apps', 'children'),
     Output('avg-rating', 'children'),
     Output('free-apps-pct', 'children')],
    [Input('app-type-filter', 'value')]
)
def update_stats(app_type):
    """
    Updates the Total Apps count, Average Rating, and Free Apps percentage
    based on the selected app type filter.
    """
    filtered_df = df if app_type == 'all' else df[df['Type'] == app_type]
    total_apps = len(filtered_df)
    avg_rating = filtered_df['Rating'].mean()
    free_apps_pct = (filtered_df['Type'] == 'Free').mean() * 100

    return (
        html.Span(f"{total_apps:,}", style={"color": "#F65725"}),
        html.Span(f"{avg_rating:.2f}" if not np.isnan(avg_rating) else "N/A", style={"color": "#197257"}),
        html.Span(f"{free_apps_pct:.1f}%", style={"color": "#FCB6C9"})
    )

@callback(
    Output('category-distribution', 'figure'),
    [Input('app-type-filter', 'value')]
)
def update_category_distribution(app_type):
    """
    Updates the Category Distribution graph based on the selected app type filter.
    """
    filtered_df = df if app_type == 'all' else df[df['Type'] == app_type]
    category_counts = filtered_df['Category'].value_counts()

    colors = ['#197257', '#F65725', '#C0DFBF', '#FCB6C9', '#F8E9A1', '#A8D0E6', '#F4A259', '#F9D4D4']
    bar_colors = [colors[i % len(colors)] for i in range(len(category_counts))]

    fig = px.bar(
        x=category_counts.index,
        y=category_counts.values,
        text=category_counts.values,
        title='Distribution of Apps by Category',
        labels={'x': 'Category', 'y': 'Number of Apps'}
    )
    fig.update_traces(
        textposition='outside',
        marker_color=bar_colors
    )
    fig.update_layout(
        xaxis_title='Category',
        yaxis_title='Number of Apps',
        margin=dict(l=40, r=40, t=40, b=80)
    )
    return fig

@callback(
    Output('rating-distribution', 'figure'),
    [Input('app-type-filter', 'value')]
)
def update_rating_distribution_side_by_side(app_type):
    """
    Updates the Average Rating by Category graph based on the selected app type filter,
    using grouped bars side-by-side for different app types.
    """
    # Apply the filter if a specific app type is selected
    filtered_df = df if app_type == 'all' else df[df['Type'] == app_type]

    grouped_ratings = filtered_df.groupby(['Category', 'Type'])['Rating'].mean().reset_index()

    type_colors = {
        'Free': '#197257',
        'Paid': '#F65725'
    }

    fig = px.bar(
        grouped_ratings,
        x='Category',
        y='Rating',
        color='Type',
        barmode='group',  # Use group mode for side-by-side bars
        title='Average Rating by Category (Grouped by App Type)',
        labels={'Rating': 'Average Rating', 'Category': 'Category', 'Type': 'App Type'},
        color_discrete_map=type_colors  # Apply custom colors
    )

    # Customize layout
    fig.update_layout(
        xaxis_title='Category',
        yaxis_title='Average Rating',
        margin=dict(l=40, r=40, t=40, b=80),
        legend_title='App Type'
    )
    return fig


@callback(
    Output('average-price-category', 'figure'),
    [Input('app-type-filter', 'value')]
)
def update_average_price_category(app_type):
    """
    Updates the Average Price by Category graph based on the selected app type filter.
    """
    filtered_df = df if app_type == 'all' else df[df['Type'] == app_type]
    filtered_df['Price'] = np.where(filtered_df['Price'] == 0, 'Free apps', filtered_df['Price'])

    avg_prices = filtered_df.groupby('Category')['Price'].apply(
        lambda x: x[x != 'Free apps'].astype(float).mean() if len(x[x != 'Free apps']) > 0 else 'Free apps'
    )

    fig = px.bar(
        x=avg_prices.index,
        y=[float(val) if val != 'Free apps' else 0 for val in avg_prices.values],
        title='Average Price by Category',
        labels={'x': 'Category', 'y': 'Average Price (USD)'}
    )
    fig.update_traces(
        marker_color='#C0DFBF'
    )
    fig.update_layout(
        xaxis_title='Category',
        yaxis_title='Average Price (USD)',
        margin=dict(l=40, r=40, t=40, b=80)
    )
    return fig


@callback(
    Output('content-rating-boxplot', 'figure'),
    [Input('app-type-filter', 'value')]
)
def update_content_rating_boxplot(app_type):
    """
    Updates the box plot visualizing the distribution of ratings
    across different content ratings, filtered by app type, with custom colors.
    """
    # Filter the data based on the selected app type
    filtered_df = df if app_type == 'all' else df.loc[df['Type'] == app_type]

    # Define custom colors for each Content Rating category
    content_rating_colors = {
        'Everyone': '#197257',
        'Teen': '#F65725',
        'Everyone 10+': '#C0DFBF',
        'Mature 17+': '#FCB6C9',
        'Adults only 18+': '#F8E9A1',
        'Unrated': '#A8D0E6'
    }

    # Create the box plot
    fig = px.box(
        filtered_df,
        x='Content_Rating',
        y='Rating',
        color='Content_Rating',
        title='The Content Rating & Rating Distribution',
        labels={'Content_Rating': 'Content Rating', 'Rating': 'Rating'},
        color_discrete_map=content_rating_colors  # Apply the custom color mapping
    )

    # Customize the layout for better visualization
    fig.update_layout(
        xaxis_title='Content Rating',
        yaxis_title='Rating',
        margin=dict(l=40, r=40, t=40, b=80),
        showlegend=False
    )

    return fig
