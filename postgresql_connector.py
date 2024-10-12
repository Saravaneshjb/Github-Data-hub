import psycopg2
import pandas as pd
import logging

class Dataload:
    def __init__(self):
        self.db_config = {#Provide the details based on the environment on which you are working or using. 
            'dbname': 'github_data_dive',
            'user': 'postgres',
            'password': 'root',
            'host': 'localhost',
            'port': 5432
        }

    def create_connection(self):
        """ Create a connection to PostgreSQL database """
        try:
            conn = psycopg2.connect(**self.db_config)
            print('Connected to PostgreSQL database')
            logging.info('Connected to PostgreSQL database')
            return conn
        except Exception as e:
            print(f"Error connecting to PostgreSQL database: {e}")
            logging.error(f"Error connecting to PostgreSQL database: {e}")
            return None

    def close_connection(self, conn):
        """ Close connection to PostgreSQL database """
        if conn:
            conn.close()
            print('Connection to PostgreSQL database closed')
            logging.info('Connection to PostgreSQL database closed')

    def execute_query(self, conn, query):
        """ Execute SQL query """
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            print("Query executed successfully")
            logging.info("Query executed successfully")
        except Exception as e:
            print(f"Error executing query: {e}")
            logging.error(f"Error executing query: {e}")

    def load_df(self, df_data, df_name):
        """ Load DataFrame to PostgreSQL """
        try:
            conn = self.create_connection()
            if conn:
                # Convert DataFrame to list of tuples
                data = [tuple(row) for row in df_data.values]
                query = f"INSERT INTO {df_name} ({', '.join(df_data.columns)}) VALUES ({', '.join(['%s'] * len(df_data.columns))})"
                print('The insert query being executed is:', query)
                logging.info(f'The insert query being executed is: {query}')
                
                cursor = conn.cursor()
                cursor.executemany(query, data)
                conn.commit()
                print("Data loaded successfully")
                logging.info("Data loaded successfully")
        finally:
            self.close_connection(conn)
    
    def read_sql(self, query):
        """ Read data from PostgreSQL into a pandas DataFrame """
        conn = self.create_connection()
        if conn:
            try:
                df = pd.read_sql(query, conn)
                print("Data fetched successfully")
                return df
            except Exception as e:
                print(f"Error reading from PostgreSQL database: {e}")
                logging.error(f"Error reading from PostgreSQL database: {e}")
            finally:
                self.close_connection(conn)
