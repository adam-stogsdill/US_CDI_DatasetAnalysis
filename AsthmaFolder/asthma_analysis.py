import pandas as pd
import matplotlib.pyplot as plt
import plotly as p
import plotly.express as px
import plotly.graph_objects as go
import os


def generate_overall_data_figures(data: pd.DataFrame, Question: str) -> None:
    # Create a dictionary for data for our first question "Hospitalizations for asthma"
    # First I want to look at the "overall" statistics for this (just for simplification)
    overall_hosp_data = data[
        (data["Question"] == Question)
        & (data["StratificationCategory1"] == "Overall")
    ]

    # Separate by year because I think it would be interesting to see the change over time
    timeline_data = {
        str(year): data[
            (data["Question"] == Question)
            & (data["StratificationCategory1"] == "Overall")
            & (data["YearStart"] == year)
            & (data["DataValueType"] == "Number")
        ]
        for year in overall_hosp_data["YearStart"].unique()
    }
    
    print(f"Question {Question}")
    # TODO: This currently opens the image inside of your browser but I feel like this
    #       could be annoying for just an analysis so I am going to change this later.
    for year in timeline_data:
        #colorbar_title = 
        print(list(timeline_data[year]['DataValueUnit'].unique()))
        
        # TODO: 
        fig = go.Figure(data=go.Choropleth(
            locations=timeline_data[year]['LocationAbbr'],
            z=timeline_data[year]['DataValue'],
            locationmode='USA-states',
            colorscale='Reds',
            autocolorscale=False,
            text=timeline_data[year]['DataValue'],
            marker_line_color="white",
            colorbar_title="Total num of instances",
            zmin=0,
            zmax=50000
        ))
        
        fig.update_layout(
            title_text = f"{Question} in {year}",
            geo = dict(
                scope='usa',
                projection=go.layout.geo.Projection(type = 'albers usa'),
                showlakes=False,
            )
        )
        
        image_name = "_".join(Question.split(" "))
        
        # Save the image
        fig.write_image(f"./figures/Asthma/overall/{image_name}_{year}.png")
    

if __name__ == "__main__":
    # Import the data (I'm going to avoid using a main file here to avoid variable scope conflicts)
    dataset = pd.read_csv("./data/topic_data/Asthma.csv")
    for question in dataset['Question'].unique():
        generate_overall_data_figures(data=dataset, Question=question)
