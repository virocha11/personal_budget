import os
import pandas as pd
import json
# from dotenv import load_dotenv
from supabase_py import create_client, Client

from configparser import ConfigParser
config = ConfigParser()
config.read('static/config/config.ini')
url: str = config.get('supabase','url')
key: str = config.get('supabase','key')

class Access_transaction:
    def __init__(self):
        self.supabase: Client=create_client(url,key)
    
    def retrieve(self, name_table, condition=None, value_condition=None):
        if(condition !=None and value_condition!=None):
            response = self.supabase.table(name_table).select().eq(condition, value_condition).execute()
            df_data = pd.DataFrame(response.get('data',[]))
            return df_data
        else:
            response = self.supabase.table(name_table).select().execute()    
            df_data = pd.DataFrame(response.get('data',[]))
            return df_data
    
    def insert(self, name_table, df_data):
        response = self.supabase.table(name_table).insert(df_data.to_dict(orient='records')).execute()
        return response 
    
    def update(self, name_table, updates, condition):
        df_updates = pd.DataFrame(updates)
        response = self.supabase.table(name_table).update(df_updates.to_dict(orient='records', condition=condition)).execute()
        return response

    def delete(self, name_table, condition ):
        response = self.supabase.table(name_table).delete(condition=condition).execute()
        return response
