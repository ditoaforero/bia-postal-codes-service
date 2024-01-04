from io import StringIO
from flask import Flask, request, jsonify
import csv
import pandas as pd
import psycopg2
import os
import uuid

# Spark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType

app = Flask(__name__)
spark = SparkSession.builder.appName("postcodes").master("local[*]").config("spark.jars", "postgresql-42.5.0.jar").getOrCreate()

@app.route('/coordinates', methods=['POST'])
def upload_csv():
    try:
        if 'file' not in request.files:
            return jsonify({"message": "No se ha enviado ningún archivo CSV"}), 400

        file = request.files['file']

        uuid_file = str(uuid.uuid4())
        print("UUID: ", uuid_file)

        create_stage(file, uuid_file)
        execute_copy(uuid_file)
        delete_file(uuid_file)


        return jsonify({"message": "Archivo CSV almacenado exitosamente en la base de datos"}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 500
    

@app.route('/calculate-postcode', methods=['GET'])
def calculate_post_code():
    print("Calculando código postal")
    calculate_post_code_process()
    return jsonify({"message": "Calculando código postal"}), 200


def calculate_post_code_process():
    db_url = "jdbc:postgresql://localhost:5432/bia"
    db_properties = {
        "user": "admin",
        "password": "admin",
        "driver": "org.postgresql.Driver",
    }
    df = spark.read.jdbc(url=db_url, table='coordinates', properties=db_properties)
    df.show()
    df.printSchema()


def create_stage(file, uuid):
    if not file:
        return None
    
    csv_data = file.read().decode('utf-8')
    csv_file = StringIO(csv_data)
    csv_reader = csv.reader(csv_file)

    headers = next(csv_reader)

    df = pd.DataFrame(csv_reader, columns=headers)
    df.astype(float)

    df.to_csv(f"./stage/{uuid}.csv", index=False, header=False)


def delete_file(uuid):
    if not os.path.exists(f"./stage/{uuid}.csv"):
        return
    
    os.remove(f"./stage/{uuid}.csv")

#define a function
def execute_copy(uuid):
    file = open(f'./stage/{uuid}.csv')
    con = psycopg2.connect(database="bia",user="admin",password="admin",host="localhost",port=5432)
    cursor = con.cursor()
    cursor.copy_from(file, 'coordenadas', sep=",")
    con.commit()
    con.close()

if __name__ == '__main__':
    app.run(debug=True)
