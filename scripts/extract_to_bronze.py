import pandas as pd
import psycopg2
import os


def extract_supermarket_data():
    try:

        conn = psycopg2.connect(
            host="localhost",
            database="airflow",
            user="airflow",
            password="airflow",
            port="5432"
        )
        
        query = "SELECT * FROM supermarket_feedback"
        
        df = pd.read_sql(query, conn)
        
        os.makedirs('data/bronze', exist_ok=True)
        
        df.to_csv('data/bronze/supermarket_raw.csv', index=False)
        
        print(f"Extração concluída! {len(df)} registros salvos em data/bronze/supermarket_raw.csv")
        
        conn.close()
        
    except Exception as e:
        print(f"Erro na extração: {e}")

if __name__ == "__main__":
    extract_supermarket_data()