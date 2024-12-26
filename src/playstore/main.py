from dash import Dash, html, page_container
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    title="PLAY STORE",
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server


sidebar = html.Div(
    [
        dbc.Row(
            [
                html.Div(
                    html.Img(src="assets/logos/logo.png", style={"height": "50px"}),
                    className="d-flex justify-content-center"
                ),
                html.H6("Google Play Store Analytics", className="text-center mt-3 fw-bold text-white"),
            ],
            className="sidebar-logo mb-4",
        ),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Img(src="assets/Table.png", style={"height": "24px", "margin-right": "10px"}),
                        "Home"
                    ],
                    href="/",
                    active="exact",
                    style={"color": "white"}
                ),
                dbc.NavLink(
                    [
                        html.Img(src="assets/Database.png", style={"height": "24px", "margin-right": "10px"}),
                        "Category Analysis"
                    ],
                    href="/category-analysis",
                    active="exact",
                    style={"color": "white"}
                ),
                dbc.NavLink(
                    [
                        html.Img(src="assets/Layers.png", style={"height": "24px", "margin-right": "10px"}),
                        "Average Distribution"
                    ],
                    href="/average-distribution",
                    active="exact",
                    style={"color": "white"}
                ),
                dbc.NavLink(
                    [
                        html.Img(src="assets/Save.png", style={"height": "24px", "margin-right": "10px"}),
                        "Prediction"
                    ],
                    href="/prediction",
                    active="exact",
                    style={"color": "white"}
                ),
            ],
            vertical=True,
            pills=True,
        ),
        html.Div(
            [
                html.Span("Created by "),
                html.A(
                    "Stefan Lences",
                    href="https://github.com/steve-len",
                    target="_blank",
                    className="text-white",
                ),
                html.Br(),
                html.Span("Data Source "),
                html.A(
                    "Google Play Data",
                    href="https://www.kaggle.com/datasets/lava18/google-play-store-apps",
                    target="_blank",
                    className="text-white",
                ),
            ],
            className="subtitle-sidebar text-white",
            style={"position": "absolute", "bottom": "10px", "width": "100%"},
        ),
    ],
    className="sidebar",
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "250px",
        "padding": "20px",
        "background-color": "#1A7258",
    },
)

content = html.Div(
    [
        page_container,
    ],
    className="page-content",
    style={"padding": "20px"},
)

app.layout = html.Div([sidebar, content])

if __name__ == "__main__":
    app.run_server(debug=True)
