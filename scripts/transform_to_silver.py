from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, trim
import os


def clean_supermarket_data():

    input_path = "/opt/airflow/data/bronze/supermarket_raw.csv"
    output_path = "/opt/airflow/data/silver/supermarket_cleaned"

    spark = SparkSession.builder \
        .appName("Supermarket-Cleaning") \
        .config("spark.driver.memory", "1g") \
        .getOrCreate()

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Arquivo não encontrado na Bronze: {input_path}")

    df = spark.read.csv(input_path, header=True, inferSchema=True)

    df_cleaned = df.withColumn("produto_nome_bruto", trim(lower(col("produto_nome_bruto")))) \
                   .withColumn("setor", trim(lower(col("setor")))) \
                   .withColumn("comentario_cliente", trim(col("comentario_cliente")))

    df_cleaned.write.mode("overwrite").option("header", "true").csv(output_path)
    
    print(f"Camada SILVER processada com sucesso em: {output_path}")
    spark.stop()

if __name__ == "__main__":
    clean_supermarket_data()