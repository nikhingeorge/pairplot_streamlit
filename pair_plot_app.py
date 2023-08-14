import streamlit as st
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

root = Path("datasets")
root.mkdir(exist_ok=True)

def get_datasets():
    datasets = root.glob("*.csv")
    return list(datasets)


def upload_dataset_using_file():
    selected_file =""
    uploaded_file = st.file_uploader("Select a file to upload", type="csv")
    if uploaded_file is not None:
        data = uploaded_file.getvalue()
        path = root.joinpath(uploaded_file.name)
        path.write_bytes(data)
        selected_file = path
    return selected_file

def upload_dataset():
    st.header("Upload a new dataset")
    filePath = upload_dataset_using_file()
    return filePath

def get_cat_columns(df):
    categorical_columns = df.select_dtypes(include=['object'])
    categorical_column_names = categorical_columns.columns.tolist()
    return categorical_column_names

def visualize_dataset(path, variable):

    df = pd.read_csv(path)
    plt.tight_layout()
    fig = ""
    if variable == "None":
        fig = sns.pairplot(data=df)
    else:
        fig = sns.pairplot(data=df, hue=variable)
    st.header("Pair Plot")
    st.pyplot(fig.figure)

description = """
Application to explore the numerical columns as a pair plot.
"""

label_upload = "Upload a new Dataset"
selected_catagorical_variable = ""

with st.sidebar:
    st.title("Pair Plot")
    st.markdown(description)
    st.header("Select a Dataset")

    options = [label_upload] + get_datasets()
    path = st.selectbox("Select a dataset", options)

    if path != label_upload:
        df = pd.read_csv(path)
        selected_catagorical_variable = st.selectbox("Color By", ["None"] + get_cat_columns(df))
        


if path == label_upload:
    newFile = upload_dataset()
    if newFile:
        with st.sidebar:
            df_new = pd.read_csv(newFile)
            selected_catagorical_variable = st.selectbox("Color By", ["None"] + get_cat_columns(df_new))
        visualize_dataset(newFile, selected_catagorical_variable)
        
else:
    visualize_dataset(path, selected_catagorical_variable)
