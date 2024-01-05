import csv
import pandas as pd
import os
from io import StringIO


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
    df.to_csv(f"./stage/{uuid}.csv", index=False, header=False)


def delete_file(uuid):
    if not os.path.exists(f"./stage/{uuid}.csv"):
        return
    os.remove(f"./stage/{uuid}.csv")
