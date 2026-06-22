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
    data = data.rename(columns={'X_Y_Co_ordinate_1': 'coordinate_1'})
    data = data.rename(columns={'X_Y_Co_ordinate_2': 'coordinate_2'})
    data = data.rename(columns={'ObjectId': 'object_id'})
    data = data.rename(columns={'Sub_Council': 'code'}).assign(sub_council=lambda x: 'Sub-Council ' + x['code'])

    # date format
    data["Created_On_Date"] = pd.to_datetime(data["Created_On_Date"], unit="ms").fillna(pd.Timestamp("1970-01-01"))    
    data["Changed_on"] = pd.to_datetime(data["Changed_on"], unit="ms").fillna(pd.Timestamp("1970-01-01"))
    data["Completed_Date"] = pd.to_datetime(data["Completed_Date"], unit="ms").fillna(pd.Timestamp("1970-01-01"))
    

    data["Created_On_Date"] = pd.to_datetime(data["Created_On_Date"], unit="ms").dt.date
    data["Changed_on"] = pd.to_datetime(data["Changed_on"], unit="ms").dt.date
    data["Completed_Date"] = pd.to_datetime(data["Completed_Date"], unit="ms").dt.date
    

    data = data.sort_values(by="Created_On_Date")
    data.columns = data.columns.str.lower()
    print(data)
    return data

rawdata = Fetch_Data(url)
dataFrame_Data = DF_Data(rawdata)
Clean_Data(dataFrame_Data)

# if __name__ == "__main__":
#     rawdata = Fetch_Data(url)
#     dataFrame_Data = DF_Data(rawdata)
#     Clean_Data(dataFrame_Data)