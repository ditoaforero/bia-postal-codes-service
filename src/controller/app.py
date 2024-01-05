import logging
import uuid
from flask import Flask, request, jsonify
from controller.utils import create_stage, delete_file
from infrastructure.aws_sqs import send_sqs_message
from infrastructure.database import PostalCodeDB

app = Flask(__name__)


@app.route('/coordinates', methods=['POST'])
def upload_csv():
    uuid_file = str(uuid.uuid4())
    try:
        if 'file' not in request.files:
            return jsonify({"message": "No se ha enviado ningún archivo CSV"}), 400
        file = request.files['file']

        create_stage(file, uuid_file)
        PostalCodeDB().copy_file_to_db(uuid=uuid_file)
        delete_file(uuid_file)
        return jsonify({"message": "Archivo CSV almacenado exitosamente en la base de datos"}), 200
    except Exception as e:
        print(e)
        logging.error(e)
        delete_file(uuid_file)
        return jsonify({"message": str(e)}), 500


@app.route('/calculate-postcode', methods=['GET'])
def calculate_post_code():
    logging.debug("calculate_post_code")
    message = {"uuid": str(uuid.uuid4())}
    send_sqs_message(message)
    return jsonify({"message": "Calculating postal code"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
