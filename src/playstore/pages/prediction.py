"""
Prediction Page Dash Application
================================

This Dash application provides a user interface to predict the category of an app based on user input,
such as the number of reviews, installs, and app category. The app utilizes a pre-trained RandomForestClassifier
model for predictions and processes input data with transformations and scaling.

Modules and Dependencies
------------------------
- `os`: File system operations.
- `pandas`: Data manipulation and analysis.
- `joblib`: Model persistence and loading.
- `dash`: Core framework for creating Dash apps.
- `dash_bootstrap_components`: Bootstrap styling components for Dash.
- `playstore.config`: Configuration for the application.

Category Mapping and Options
============================

The `category_mapping` dictionary maps app categories to unique numerical codes, essential for:
- **Encoding Categorical Data:** Converts categories like `"GAME"` into numbers (`17`) for machine learning models.
- **Maintaining Consistency:** Ensures predictions align with the encoding used during model training.

The `category_options` list is derived from `category_mapping` to populate the Dash dropdown:
- `label`: User-friendly category names (e.g., `"GAME"`).
- `value`: Corresponding numerical codes (e.g., `17`).

**Purpose:**
- Provides user-friendly input for selecting categories.
- Translates selections into model-compatible numerical values.
- Ensures seamless integration between the app's UI and the machine learning model.
"""

import os
import pandas as pd
import joblib
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Output, Input, State, register_page
from playstore.config import CLEAN_DATA_DIR

# Register the page
register_page(__name__, path="/prediction", name="Prediction Page")

print(CLEAN_DATA_DIR)


# Load the model
try:

    print("Model loaded successfully.")
    expected_features = ["Reviews", "Installs", "Category_encoded"]
    df = pd.read_csv(os.path.join(CLEAN_DATA_DIR, "cleaned_googleplaystore.csv"))
    model = joblib.load(os.path.join(CLEAN_DATA_DIR, "rf_model_category.pkl"))

    # Define the category mapping
    category_mapping = {
        'ART_AND_DESIGN': 0, 'AUTO_AND_VEHICLES': 1, 'BEAUTY': 2, 'BOOKS_AND_REFERENCE': 3,
        'BUSINESS': 4, 'COMICS': 5, 'COMMUNICATION': 6, 'DATING': 7, 'EDUCATION': 8,
        'ENTERTAINMENT': 9, 'EVENTS': 10, 'FINANCE': 11, 'FOOD_AND_DRINK': 12,
        'HEALTH_AND_FITNESS': 13, 'HOUSE_AND_HOME': 14, 'LIBRARIES_AND_DEMO': 15,
        'LIFESTYLE': 16, 'GAME': 17, 'FAMILY': 18, 'MEDICAL': 19, 'SOCIAL': 20,
        'SHOPPING': 21, 'PHOTOGRAPHY': 22, 'SPORTS': 23, 'TRAVEL_AND_LOCAL': 24,
        'TOOLS': 25, 'PERSONALIZATION': 26, 'PRODUCTIVITY': 27, 'PARENTING': 28,
        'WEATHER': 29, 'VIDEO_PLAYERS': 30, 'NEWS_AND_MAGAZINES': 31, 'MAPS_AND_NAVIGATION': 32
    }
    category_options = [{"label": name, "value": code} for name, code in category_mapping.items()]
except Exception as e:
    model = None
    expected_features = []
    category_mapping = {}
    category_options = []
    print(f"Error loading the model: {e}")


# Layout Definition
layout = html.Div([
    dbc.Container([
        html.H1("Prediction Bonus", className="text-center text-google-play mb-4"),
        html.Ul([
            html.Li("The app's rating is categorized as Low, Medium, or High based on these thresholds:",
                    className="mb-2"),
            html.Ul([
                html.Li("Low: Rating < 3.5", className="ms-4"),
                html.Li("Medium: 3.5 ≤ Rating ≤ 4.5", className="ms-4"),
                html.Li("High: Rating > 4.5", className="ms-4")
            ]),
            html.Li("The model preprocesses input features as follows:", className="mb-2"),
            html.Ul([
                html.Li("Log transformations are applied to Reviews and Installs to handle skewed distributions.",
                        className="ms-4"),
                html.Li("A new feature, Review-to-Install Ratio, is derived to capture user engagement.",
                        className="ms-4")
            ]),
            html.Li("The data is standardized using scaling to ensure features contribute equally.", className="mb-2"),
            html.Li("A RandomForestClassifier is trained on the processed data with these settings:", className="mb-2"),
            html.Ul([
                html.Li("200 trees in the forest for robust predictions.", className="ms-4"),
                html.Li("Maximum tree depth of 20 to prevent overfitting.", className="ms-4"),
                html.Li("Class weights to balance Low, Medium, and High ratings.", className="ms-4")
            ]),
            html.Li("The model is evaluated using metrics like accuracy and a classification report.", className="mb-2")
        ], className="text-muted"),
        html.P(
            "Use the form below to predict the category of an app based on the number of reviews, installs, and category.",
            className="text-center text-muted"),
        dbc.Row([
            dbc.Col([
                html.Label("Reviews", className="me-2"),
                dcc.Input(id="reviews", type="number", value=1500, placeholder="Enter Reviews", className="me-3"),
                html.Label("Installs", className="me-2"),
                dcc.Input(id="installs", type="number", value=50000, placeholder="Enter Installs", className="me-3"),
                html.Label("Category", className="me-2"),
                dcc.Dropdown(
                    id="category_dropdown",
                    options=category_options,
                    value=0,
                    placeholder="Select a category",
                    style={"width": "250px", "display": "inline-block"}
                )
            ], width=12, className="d-flex align-items-center justify-content-center")
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Button("Predict", id="predict_button", color="primary", className="mt-3")
            ], width=12, className="text-center")
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                html.Div(id="prediction_output", className="mt-4 text-center")
            ], width=12)
        ])
    ])
])

# Callback for Prediction
@callback(
    Output("prediction_output", "children"),
    Input("predict_button", "n_clicks"),
    State("reviews", "value"),
    State("installs", "value"),
    State("category_dropdown", "value")
)
def make_prediction(n_clicks, reviews, installs, category_encoded):
    """
    Handles predictions for app categories.

    Parameters:
    -----------
    - `n_clicks`: Number of button clicks.
    - `reviews`: Number of reviews entered by the user.
    - `installs`: Number of installs entered by the user.
    - `category_encoded`: Encoded category value selected by the user.

    Returns:
    --------
    A message with the prediction result or an error alert if an issue occurs.
    """
    if n_clicks is None:
        return "Enter values and click Predict."

    if model is None:
        return "Model is not loaded. Check if the model file exists at the specified path."

    try:
        # Input validation
        if not isinstance(reviews, (int, float)) or reviews <= 0:
            return dbc.Alert("Reviews must be a positive number.", color="warning")
        if not isinstance(installs, (int, float)) or installs <= 0:
            return dbc.Alert("Installs must be a positive number.", color="warning")
        if category_encoded not in category_mapping.values():
            return dbc.Alert("Invalid category selected.", color="warning")

        # Prepare input data
        input_data = pd.DataFrame([{
            "Reviews": reviews,
            "Installs": installs,
            "Category_encoded": category_encoded
        }], columns=expected_features)

        # Feature alignment
        input_data = input_data[model.feature_names_in_]

        # Make prediction
        prediction_encoded = model.predict(input_data)

        # Decode the prediction
        categories = ["Low", "Medium", "High"]
        prediction_decoded = categories[int(prediction_encoded[0])]

        return dbc.Alert(f"Prediction: {prediction_decoded}", color="success")
    except Exception as e:
        return dbc.Alert(f"Error during prediction: {e}", color="danger")
