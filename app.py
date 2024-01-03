from io import StringIO
from flask import Flask, request, jsonify
import csv
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType

app = Flask(__name__)
spark = SparkSession.builder.appName("CSV to Spark Dataframe").master("local[*]").config("spark.jars", "postgresql-42.5.0.jar").getOrCreate()

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    try:
        if 'file' not in request.files:
            return jsonify({"message": "No se ha enviado ningún archivo CSV"}), 400

        file = request.files['file']

        df_coordinates = create_data_frame_spark(file)

        write_database("coordinates", df_coordinates, 10)
            
        return jsonify({"message": "Archivo CSV almacenado exitosamente en la base de datos"}), 200

    

        df_coordinates = create_data_frame(spark, file)
        if not df_coordinates:
            return jsonify({"message": "El CSV no dispone de una buena información"}), 400

        write_database("coordinates", df_coordinates, 2)
            
        return jsonify({"message": "Archivo CSV almacenado exitosamente en la base de datos"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    


def create_data_frame(spark, file):
    if not file:
        return None
    
    csv_data = file.read().decode('utf-8')
    csv_file = StringIO(csv_data)
    csv_reader = csv.reader(csv_file)

    headers = next(csv_reader)


    df = pd.DataFrame(csv_reader, columns=headers)

    schema = StructType([
        StructField("lat", DoubleType(), True),
        StructField("lon", DoubleType(), True),
    ])
            
    return spark.createDataFrame(df, schema=schema)


def write_database(table_name, df, partition_amount):
    db_url = "jdbc:postgresql://localhost:5432/bia"
    db_properties = {
        "user": "admin",
        "password": "admin",
        "driver": "org.postgresql.Driver"
    }

    df_to_write = df.repartition(partition_amount)

    df_to_write.write.jdbc(url=db_url, table=table_name, mode="overwrite", properties=db_properties)

def create_data_frame_spark(file):
    csv_data = file.read().decode('utf-8')

    # Read CSV using Spark
    df = spark.read.csv(spark.sparkContext.parallelize([csv_data]))

    return df

    
if __name__ == '__main__':
    app.run(debug=True)
