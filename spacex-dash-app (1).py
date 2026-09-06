# Import required libraries
import dash
import pandas as pd
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()


# Create a dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={
                "textAlign": "center",
                "color": "#503D36",
                "font-size": 40
            }
        ),

        # TASK 1: Add a dropdown list to enable Launch Site selection
        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "ALL"},
                {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
                {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"}
            ],
            value="ALL",
            placeholder="Select a Launch Site here",
            searchable=True
        ),

        html.Br(),

        # TASK 2: Pie chart
        html.Div(
            dcc.Graph(id="success-pie-chart")
        ),

        html.Br(),

        html.P("Payload range (Kg):"),

        # TASK 3: Range Slider
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            marks={
                0: "0",
                2500: "2500",
                5000: "5000",
                7500: "7500",
                10000: "10000"
            },
            value=[min_payload, max_payload]
        ),

        # TASK 4: Scatter chart
        html.Div(
            dcc.Graph(id="success-payload-scatter-chart")
        )
    ]
)


# TASK 2:
# Callback for site-dropdown and success-pie-chart

@app.callback(
    Output(
        component_id="success-pie-chart",
        component_property="figure"
    ),
    Input(
        component_id="site-dropdown",
        component_property="value"
    )
)
def get_pie_chart(entered_site):

    if entered_site == "ALL":
        success_df = spacex_df[spacex_df["class"] == 1]

        fig = px.pie(
            success_df,
            names="Launch Site",
            title="Total Success Launches by Site"
        )

    else:
        site_df = spacex_df[
            spacex_df["Launch Site"] == entered_site
        ]

        success_count = site_df["class"].value_counts().to_dict()

        success_failed_df = pd.DataFrame({
            "Outcome": ["Failure", "Success"],
            "Count": [
                success_count.get(0, 0),
                success_count.get(1, 0)
            ]
        })

        fig = px.pie(
            success_failed_df,
            values="Count",
            names="Outcome",
            title="Total Success Launches for " + entered_site
        )

    return fig


# TASK 4:
# Callback for site-dropdown and payload-slider

@app.callback(
    Output(
        component_id="success-payload-scatter-chart",
        component_property="figure"
    ),
    [
        Input(
            component_id="site-dropdown",
            component_property="value"
        ),
        Input(
            component_id="payload-slider",
            component_property="value"
        )
    ]
)
def get_scatter_chart(entered_site, payload_range):

    low, high = payload_range

    if entered_site == "ALL":
        filtered_df = spacex_df
        title = "Correlation between Payload and Success for All Sites"

    else:
        filtered_df = spacex_df[
            spacex_df["Launch Site"] == entered_site
        ]
        title = "Correlation between Payload and Success for " + entered_site

    filtered_df = filtered_df[
        (filtered_df["Payload Mass (kg)"] >= low)
        & (filtered_df["Payload Mass (kg)"] <= high)
    ]

    fig = px.scatter(
        filtered_df,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        title=title
    )

    return fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True)