import unittest
import pandas as pd
from data_pipeline.transform import Transform_Data

class TestTransformData(unittest.TestCase):

    def test_dataframe_creation(self):
        self.data = {
                    "type": "FeatureCollection",
                    "properties": {
                        "exceededTransferLimit": True
                    },
                    "features": [
                        {
                        "type": "Feature",
                        "id": 1,
                        "geometry": None,
                        "properties": {
                            "Sub_Council": "0",
                            "Ward": "000",
                            "Suburb": "GENERIC TOWN 0000",
                            "C3_Complaint_Type": "No Power",
                            "Work_Center": "Electricity - FLR-Gugulethu-Contractor",
                            "Notification": 1023307365,
                            "Notification_type": "1023307365",
                            "X_Y_Co_ordinate_1": 0,
                            "X_Y_Co_ordinate_2": 0,
                            "Created_On_Date": 1776290400000,
                            "Changed_on": 1776290400000,
                            "Completed_Date": 1776290400000,
                            "Notifications_Created": 1,
                            "ObjectId": 1
                        }
                        },
                        {
                        "type": "Feature",
                        "id": 2,
                        "geometry": None,
                        "properties": {
                            "Sub_Council": "0",
                            "Ward": "000",
                            "Suburb": "GENERIC TOWN 0000",
                            "C3_Complaint_Type": "No Power",
                            "Work_Center": "Electricity - FLR-Gugulethu-Contractor",
                            "Notification": 1023335825,
                            "Notification_type": "SAP DOWNTIME MANUAL REF PM030",
                            "X_Y_Co_ordinate_1": 0,
                            "X_Y_Co_ordinate_2": 0,
                            "Created_On_Date": 1776895200000,
                            "Changed_on": 1777413600000,
                            "Completed_Date": 1777413600000,
                            "Notifications_Created": 1,
                            "ObjectId": 2
                        }
                        }
                    ]
                    }
                
        
        df = Transform_Data(self.data)
        # Check type
        self.assertIsInstance(df, pd.DataFrame)
        # Check number of rows
        self.assertEqual(len(df), 2)
        # Check columns exist
        self.assertIn("Suburb", df.columns)
        self.assertIn("C3_Complaint_Type", df.columns)
        # Check values
        self.assertEqual(df.loc[0, "Suburb"], "GENERIC TOWN 0000")
        self.assertEqual(df.loc[1, "C3_Complaint_Type"], "No Power")
        
if __name__ == "__main__":
    unittest.main()