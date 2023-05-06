import pandas as pd
import matplotlib.pyplot as plt
import plotly as p



def run_analysis(file_location):
    full_dataset = pd.read_csv(file_location)
    print(full_dataset.head())


if __name__ == "__main__":
    run_analysis(file_location="./U.S._Chronic_Disease_Indicators__CDI_.csv")