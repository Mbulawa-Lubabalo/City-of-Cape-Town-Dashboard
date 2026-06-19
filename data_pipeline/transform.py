from data_pipeline.ingestion import Fetch_Data
import pandas as pd
import json


url = "https://services6.arcgis.com/nyYfO9SxHU2ChQd9/arcgis/rest/services/Service_Requests_2023_until_20_May_2026/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"


def DF_Data(rawdata: dict) -> pd.DataFrame:
    features = rawdata["features"]
    
    df = pd.DataFrame([f["properties"] for f in features])
    
    print(df.head())
    return df

def Clean_Data(data: pd.DataFrame):
    # Rename columns
    data = data.rename(columns={'C3_Complaint_Type': 'Complaint_Type'})

    
    print(data)
    return data

if __name__ == "__main__":
    rawdata = Fetch_Data(url)
    dataFrame_Data = DF_Data(rawdata)
    Clean_Data(dataFrame_Data)