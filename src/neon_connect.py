import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine

class DatabaseManager:
    def __init__(self):
        # 1. Explicitly find the .env file in the root directory
        # __file__ is the path to this script (inside src/)
        # .parent goes up one level to the project root
        env_path = Path(__file__).parent.parent / '.env'
        
        # 2. Load the environment variables from that specific path
        load_dotenv(dotenv_path=env_path)
        
        # 3. Extract the URL
        self.database_url = os.getenv("DATABASE_URL")
        
        # 4. Check if it exists
        if not self.database_url:
            raise ValueError(f"DATABASE_URL not found. Checked path: {env_path}")
        
        # 5. Create the engine
        self.engine = create_engine(self.database_url)
        print("✅ Successfully connected to Neon PostgreSQL database.")

    def upload_dataframe(self, df, table_name, if_exists='replace'):
        """Uploads a pandas DataFrame to the Neon database."""
        df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
        print(f"✅ Successfully uploaded {len(df)} rows to '{table_name}'.")

    def fetch_dataframe(self, query):
        """Fetches data from the database using a SQL query."""
        import pandas as pd
        return pd.read_sql(query, self.engine)