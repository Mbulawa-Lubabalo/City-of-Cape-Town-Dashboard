from data_pipeline.ingestion import Fetch_Data
import pandas as pd
import json


url = "https://services6.arcgis.com/nyYfO9SxHU2ChQd9/arcgis/rest/services/Service_Requests_2023_until_20_May_2026/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"


def Transform_Data(rawdata: dict):
    features = rawdata["features"]
    
    df = pd.DataFrame([f["properties"] for f in features])
    
    print(df.head())
    return df


if __name__ == "__main__":
    rawdata = Fetch_Data(url)
    Transform_Data(rawdata)