import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv


class Fetcher:
    def __init__(self):
        load_dotenv()
        self.uri = os.getenv("MONGO_URL")
        self.client = MongoClient(self.uri)
        self.db = self.client["IranMalDB"]
        self.collection = self.db["tweets"]
        self.data = self._fetch_data()

    def _fetch_data(self) -> pd.DataFrame:
        documents = list(self.collection.find({}, {"_id": 0}))
        df = pd.DataFrame(documents)
        return df


    def get_documents(self) -> pd.DataFrame:
        return self.data

    def connect(self):
        try:
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
            return self.client
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            return None

    def close_connection(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed")