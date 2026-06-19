import requests

url = "https://services6.arcgis.com/nyYfO9SxHU2ChQd9/arcgis/rest/services/Service_Requests_2023_until_20_May_2026/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

def Fetch_Data(url: str):

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=HEADERS, timeout=10)
    return response.json()

if __name__ == "__main__":
    print(type(Fetch_Data(url)))

