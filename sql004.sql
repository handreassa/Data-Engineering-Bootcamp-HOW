from sqlalchemy import create_engine
engine = create_engine('postgresql+pyscopg2://user:password@hostname/database_name')