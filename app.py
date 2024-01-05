from io import StringIO
from flask import Flask, request, jsonify
import csv
import pandas as pd
import psycopg2
import os
import uuid
import requests
import json
from pyspark.sql import Row
import boto3


# Spark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType, StringType

app = Flask(__name__)
spark = SparkSession.builder.appName("postcodes").master("local[*]").config("spark.jars", "postgresql-42.5.0.jar").getOrCreate()

@app.route('/coordinates', methods=['POST'])
def upload_csv():
    try:
        if 'file' not in request.files:
            return jsonify({"message": "No se ha enviado ningún archivo CSV"}), 400

        file = request.files['file']

        uuid_file = str(uuid.uuid4())

        create_stage(file, uuid_file)
        execute_copy(uuid_file)
        delete_file(uuid_file)


        return jsonify({"message": "Archivo CSV almacenado exitosamente en la base de datos"}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 500
    

@app.route('/calculate-postcode', methods=['GET'])
def calculate_post_code():
    df = get_df_coordinates()
    get_post_code(df)

    return jsonify({"message": "Calculando código postal"}), 200


def get_df_coordinates():
    db_url = "jdbc:postgresql://localhost:5432/bia"
    db_properties = {
        "user": "admin",
        "password": "admin",
        "driver": "org.postgresql.Driver",
    }

    return spark.read.jdbc(url=db_url, table='coordinates', properties=db_properties)


def process_partition(iterator):
    geolocations = []
    for row in iterator:
        print(row)
        geolocations.append({
            "latitude": row.lat,
            "longitude": row.lon,
            "limit": 1
        })

    payload = {
        "geolocations": geolocations
    }

    send_message(payload)
    

def get_post_code(df):
    batch_size = 100

    df_repartition = df.repartition(df.count() // batch_size + 1)

    # numero de particiones que tiene el dataframe
    #print("Numero de particiones:", df.rdd.getNumPartitions())

    df_repartition.foreachPartition(process_partition)

    #write_df_to_db(df_final)

    


def write_df_to_db(df):
    db_url = "jdbc:postgresql://localhost:5432/bia"
    db_properties = {
        "user": "admin",
        "password": "admin",
        "driver": "org.postgresql.Driver",
    }
    df.write.jdbc(url=db_url, table='coordinates', properties=db_properties, mode='overwrite')

def create_stage(file, uuid):
    if not file:
        return None
    
    csv_data = file.read().decode('utf-8')
    csv_file = StringIO(csv_data)
    csv_reader = csv.reader(csv_file)

    headers = next(csv_reader)

    df = pd.DataFrame(csv_reader, columns=headers)
    df.astype(float)
    df.drop_duplicates(inplace=True)
    df['postcode'] = None

    print(df)

    df.to_csv(f"./stage/{uuid}.csv", index=False, header=False)


def delete_file(uuid):
    if not os.path.exists(f"./stage/{uuid}.csv"):
        return
    
    os.remove(f"./stage/{uuid}.csv")

def process_row(row, cur_merge):
    sql_string = "UPDATE coordinates SET postcode = %s WHERE lat = %s AND lon = %s", (row.postcode, row.lat, row.lon)
    cur_merge.execute(sql_string)

#define a function
def execute_copy(uuid):
    file = open(f'./stage/{uuid}.csv')
    con = psycopg2.connect(database="bia",user="admin",password="admin",host="localhost",port=5432)
    cursor = con.cursor()
    cursor.copy_from(file, 'coordinates', sep=",")
    con.commit()
    con.close()


def send_message(message):
    sqs_client = boto3.client("sqs", endpoint_url="http://localhost:4566")

    response = sqs_client.send_message(
        QueueUrl="http://localhost:4566/000000000000/test",
        MessageBody=json.dumps(message)
    )
    print(response)

if __name__ == '__main__':
    app.run(debug=True)


