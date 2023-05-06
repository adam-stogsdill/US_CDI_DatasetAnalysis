import pandas as pd
import matplotlib.pyplot as plt
import plotly as p
import plotly.express as px
import os

# Import the data (I'm going to avoid using a main file here to avoid variable scope conflicts)
data = pd.read_csv("./data/topic_data/Asthma.csv")

# Create a dictionary for data for our first question "Hospitalizations for asthma"
# First I want to look at the "overall" statistics for this (just for simplification)
overall_hosp_data = data[
    (data["Question"] == "Hospitalizations for asthma")
    & (data["StratificationCategory1"] == "Overall")
]

# Separate by year because I think it would be interesting to see the change over time
timeline_data = {
    str(year): data[
        (data["Question"] == "Hospitalizations for asthma")
        & (data["StratificationCategory1"] == "Overall")
        & (data["YearStart"] == year)
        & (data["DataValueType"] == "Number")
    ]
    for year in overall_hosp_data["YearStart"].unique()
}

# generate a list of the keys in order
keys = list(timeline_data.keys())
keys.sort()

# TODO: This currently opens the image inside of your browser but I feel like this
#       could be annoying for just an analysis so I am going to change this later.
for year in keys:
    fig = px.choropleth(
        timeline_data[year],
        locations="LocationAbbr",
        color="DataValue",
        color_continuous_scale="spectral_r",
        hover_name="LocationDesc",
        locationmode="USA-states",
        labels={f"Number of Hospitalization for Asthma in {year}"},
        scope="usa",
        range_color=[0, 50000],
    )

    fig.add_scattergeo(
        locations=timeline_data[year]["LocationAbbr"],
        locationmode="USA-states",
        text=timeline_data[year]["LocationAbbr"],
        mode="text",
    )

    fig.update_layout(
        title={
            "text": f"Number of Hospitalization for Asthma in {year}",
            "xanchor": "center",
            "yanchor": "top",
            "x": 0.5,
        }
    )

    fig.show()


data_hosp = data[
    (data["Question"] == "Hospitalizations for asthma")
    & (data["StratificationCategory1"] == "Overall")
    & (data["YearStart"] == year)
    & (data["DataValueType"] == "Number")
]

data_hosp.sort_values(by='YearStart')

fig = px.choropleth(
    data_hosp,
    locations="LocationAbbr",
    color="DataValue",
    color_continuous_scale="spectral_r",
    hover_name="LocationDesc",
    locationmode="USA-states",
    animation_frame='YearStart',
    animation_group="LocationAbbr",
    labels={f"Number of Hospitalization for Asthma by Year"},
    scope="usa",
    range_color=[0, 50000],
)

fig.add_scattergeo(
    locations=data_hosp["LocationAbbr"],
    locationmode="USA-states",
    text=data_hosp["LocationAbbr"],
    mode="text",
)

fig.update_layout(
    title={
        "text": f"Number of Hospitalization for Asthma by Year",
        "xanchor": "center",
        "yanchor": "top",
        "x": 0.5,
    }
)

fig.show()
