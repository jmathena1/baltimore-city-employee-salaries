####code gathered from Phil Hather (https://philhather.medium.com/loading-api-data-into-google-bigquery-with-cloud-functions-and-scheduler-ffc4a74b2e05)####
####Stack Overflow code from https://stackoverflow.com/questions/56958209/turning-json-into-dataframe-with-pandas####

import urllib3
import json
import pandas as pd
from math import ceil
from google.cloud import storage

C_OBJECT_IDS_URL = 'https://services1.arcgis.com/UWYHeuuJISiGmgXx/arcgis/rest/services/Baltimore_City_Employee_Salaries_New/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&returnIdsOnly=true&f=json'
C_SALARIES_URL = 'https://services1.arcgis.com/UWYHeuuJISiGmgXx/arcgis/rest/services/Baltimore_City_Employee_Salaries_New/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&objectIds={}&f=json'
BATCH = 200

# query open baltimore data api for all object ids of city employee salaries dataset
def get_object_ids(url):
    object_id_json = urllib3.PoolManager().request('GET', url)
    return json.loads(object_id_json.data.decode('utf-8'))["objectIds"]

# query open baltimore data api for all salary records in batches of 200 records
def get_salary_data(ids, url):
    runs = ceil(len(ids) / BATCH)
    city_salaries = []

    for run in range(0, runs):
        idx = run * BATCH
        idx_to = idx + (BATCH if run < runs - 1 else len(ids) -  BATCH * run)
        print(f"Sending batch {run + 1}/{runs}: requesting salary records {idx}, {idx_to}")

        try:
            url_batch = ", ".join(map(str, ids[idx:idx_to]))
            salaries_url = url.format(url_batch)
            salaries_json = urllib3.PoolManager().request('GET', salaries_url)
            raw_salaries_json = json.loads(salaries_json.data.decode('utf-8'))
            formatted_json = [feature['attributes'] for feature in raw_salaries_json['features']]
            city_salaries.extend(formatted_json)
        except Exception as e:
            print(f"ERROR in API call run {run + 1}: {e}")
    return city_salaries

# upsert a Pandas dataframe of salary data to data bucket in google cloud
def upsert_salary_data(df):
    bucket = storage.Client(project='open-baltimore-data').get_bucket('open-baltimore-data')
    blob = bucket.blob('city_employee_salaries.csv')
    #upload blob to open baltimore data bucket
    blob.upload_from_string(pd.DataFrame(df).to_csv(index = False), content_type = 'csv')

def main():
    city_salaries_df = get_salary_data(get_object_ids(C_OBJECT_IDS_URL), C_SALARIES_URL)
    upsert_salary_data(city_salaries_df)

if __name__ == "__main__":
    main()