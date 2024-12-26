from dash import html, register_page

register_page(__name__, path="/", name="Domov")

layout = html.Div(
    [
        html.H1("Welcome to Google Play Store Analytics", className="text-center mt-5 text-google-play"),
        html.P(
            "This dataset contains comprehensive information about applications available on Google Play Store, "
            "including their categories, user ratings, number of reviews, number of installs, prices, "
            "content ratings, genres, and update history. It provides valuable insights for understanding "
            "app trends, user preferences, and performance metrics.",
            className="text-center mt-2", style={"paddingLeft": "10%", "paddingRight": "10%"}
        ),
        html.Div([
            html.Img(src="/assets/googleplaystore.jpg", alt="Google Play Store Analytics",
                     className="img-fluid mt-4", style={"maxWidth": "60%", "margin": "0 auto"})
        ], className="text-center container mt-10"),
        html.Div(
            [
                html.Span("Created by "),
                html.A(
                    "Stefan Lences",
                    href="https://github.com/steve-len",
                    target="_blank",
                    className="text-black",
                ),
                html.Br(),
                html.Span("Data Source "),
                html.A(
                    "Google Play Data",
                    href="https://www.kaggle.com/datasets/lava18/google-play-store-apps",
                    target="_blank",
                    className="text-black",
                ),
            ],
            className="text-center text-black mt-5",
        ),
    ],
    className="container",
)
