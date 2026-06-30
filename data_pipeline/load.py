from supabase import create_client, Client
from data_pipeline.transform import Clean_Data, dataFrame_Data
from sqlalchemy import create_engine, text
from database import Database_management, Insert_data, vw_service_requests, queries
# from data_pipeline.ingestion import Fetch_Data

def Database_Connection():
    DB_URL = "postgresql://postgres.sopoxavbgzasekfzjyrb:Lmbulawa4%40006@aws-0-eu-west-1.pooler.supabase.com:5432/postgres"
    # print(DB_URL)
    
    if not DB_URL:
        raise RuntimeError("DATABASE_URL environment variable not set")
    engine = create_engine(DB_URL, pool_pre_ping=True)
    return engine

def Load_Data(engine):

    key = "sb_publishable_cQfxPy_Jturhljr9sxlZbw__xTz7Z4Q"
    
    # supabase: Client = create_client(url, key)
    # print(supabase)
    # records = df.to_dict(orient="records")
    # # print(records)
    # supabase.table("service_requests").insert(records).execute()
    Database_management(engine)

if __name__=="__main__":
    engine = Database_Connection()
    # print(engine)
    df = Clean_Data(dataFrame_Data)
    # Load_Data(engine)
    # Insert_data(engine, df)
    # vw_service_requests(engine)
    queries(engine)