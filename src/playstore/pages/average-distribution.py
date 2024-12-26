"""
Average Distribution Dash Application
=====================================

This Dash application provides insights into the average distribution of Google Play Store app ratings.
Users can filter by category and app type (Free or Paid) to analyze the rating distribution and density.

The application is built with Dash, Plotly, and Bootstrap, providing interactive filtering and visualization.

Modules and Dependencies
------------------------
- `os`: File system operations.
- `pandas`: Data manipulation and analysis.
- `numpy`: Numerical operations and array manipulations.
- `dash`: Core framework for creating Dash apps.
- `dash_bootstrap_components`: Bootstrap styling components for Dash.
- `plotly.express`: Simplified interface for Plotly visualizations.
- `playstore.config`: Configuration for the application.
- `plotly.graph_objects`: Low-level interface for creating Plotly visualizations.
"""

import os
import pandas as pd
import numpy as np
from dash import html, dcc, callback, Output, Input, register_page
import dash_bootstrap_components as dbc
import plotly.express as px
from playstore.config import CLEAN_DATA_DIR
import plotly.graph_objects as go

# Page Registration
register_page(__name__, path="/average-distribution", name="Success Prediction")

# Load Data
df = pd.read_csv(os.path.join(CLEAN_DATA_DIR, "cleaned_googleplaystore.csv"))

# Layout Definition
layout = html.Div(
  [
      html.H1("Average Distribution", className="text-google-play text-center mb-4"),
      html.Div([
          html.H3("Filters", className="h5 mb-3 fw-bold"),
          dcc.Dropdown(
              id='category-filter',
              options=[{'label': cat, 'value': cat} for cat in sorted(df['Category'].unique())],
              value=None,
              placeholder="Select a category",
              className="form-select mb-3"
          ),
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
          dcc.Graph(id="user-ratings-distribution"),
      ], className="mb-4")
  ],
  className="container",
)

# Callback to Update Distribution Graph
@callback(
  Output('user-ratings-distribution', 'figure'),
  [Input('category-filter', 'value'),
   Input('app-type-filter', 'value')]
)
def update_user_ratings_distribution(selected_category, app_type):
    """
     Updates the user rating distribution histogram and density plot based on the selected category and app type filter.

     Parameters:
     -----------
     - `selected_category`: The selected category filter from the dropdown.
     - `app_type`: The selected app type filter (All, Free, Paid).
     """
    filtered_df = df.copy()
    if selected_category:
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
    if app_type != 'all':
        filtered_df = filtered_df[filtered_df['Type'] == app_type]

    fig = px.histogram(
        filtered_df,
        x='Rating',
        title='The Distribution of User Ratings',
        labels={'x': 'Rating', 'y': 'Count'},
        nbins=20,
        opacity=0.7
    )
    fig.update_traces(marker_color='#197257', marker_line_width=0.5)

    density = filtered_df['Rating'].value_counts(normalize=True).sort_index()
    fig.add_trace(
        go.Scatter(
            x=density.index,
            y=density.values * len(filtered_df),
            mode='lines',
            line=dict(color='blue', width=2),
            name='Density'
        )
    )

    fig.update_layout(
        xaxis_title='Rating',
        yaxis_title='Count',
        margin=dict(l=40, r=40, t=40, b=80),
        showlegend=True
    )
    return fig
