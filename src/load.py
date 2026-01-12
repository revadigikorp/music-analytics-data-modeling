from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def load_to_db(df, table_name, engine):
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False, method='multi')
    except SQLAlchemyError as e:
        print(f"Error loading {table_name}: {e}")