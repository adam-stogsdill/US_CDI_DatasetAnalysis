"""
This is essentially a script designed to generate the data
that I am going to use for the analysis of the data.

The goal is to simplify the process by removing the amount
of querying that I have to do to generate these bits of data
and I can simply load it in using the specific file tree structure.
"""
import pandas as pd
import matplotlib.pyplot as plt
import plotly as p
import os


def initial_preprocessing(file_location: str) -> pd.DataFrame:
    """ This initial preprocessing step to the whole dataset
        will make it easier to manipulate the data.
        
        I did notice in my analysis in the Jupyter Notebook
        that there were columns in the data that contained
        almost all NULL/NAN values so those are the ones
        that I drop.

    Args:
        file_location (str): The location of the data.

    Returns:
        pd.DataFrame: The cleaned data.
    """    
    full_dataset = pd.read_csv(file_location)
    # print(full_dataset.head())

    # Drop unnecessary columns
    full_dataset.drop(
        columns=[
            "Response",
            "StratificationCategory2",
            "StratificationCategory3",
            "Stratification3",
            "ResponseID",
            "StratificationCategoryID2",
            "StratificationID2",
            "StratificationCategoryID3",
            "StratificationID3",
        ],
        inplace=True,
    )

    return full_dataset


def generate_dataset_config(
    data: pd.DataFrame, file_location: str = "./dataset_configuration.txt"
) -> None:
    """ Generates the dataset configuration text file that details some
        of the information given and helps a bit with navigating the large
        dataset file.
        
        If the column's data type is an "object" I record the unique values.
        Otherwise, I use pandas' describe method to give the basic statistics
        one the data, assuming it is quantitative information.

    Args:
        data (pd.DataFrame): The data for generating the dataset_config file.
        file_location (str, optional): The file location. Defaults to "./dataset_configuration.txt".
    """    
    # Create a file that details the configuration of the data.
    with open(file_location, "w", encoding="utf-8") as file:       # Output this to a file so that 
        for col, dtype in zip(data, data.dtypes):
            file.write(f"{col}\t\t{dtype}\n")
            if dtype == object:
                file.write(f"{str(data[col].unique())}\n")
            else:
                file.write(f"{str(data[col].describe())}\n")
            file.write("\n")
            

def run_data_gen(file_location: str) -> None:
    data = initial_preprocessing(file_location)
    
    # generate a document that will give us a little insight on the
    # structure of the data.
    generate_dataset_config(data)
    
    # split by topic
    topic_dict = {topic: data[data['Topic'] == topic] for topic in data['Topic'].unique()}
    
    # Generate the CSVs for caching data later.
    for topic in topic_dict:
        topic_dict[topic].to_csv(f"./data/topic_data/{topic}.csv")

if __name__ == "__main__":
    run_data_gen(file_location="./U.S._Chronic_Disease_Indicators__CDI_.csv")
