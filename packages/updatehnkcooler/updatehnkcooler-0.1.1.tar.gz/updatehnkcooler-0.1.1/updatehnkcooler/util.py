import json
import datetime, pytz
from datetime import datetime as dt
from google.cloud import bigquery
import uuid
from google.cloud import storage
import logging


# ----------------------------------------------------------------------------------------------------------------------
def get_tmp_table_name(config: dict) -> str:
    prefix = "tmp"
    suffix = str(uuid.uuid4().hex)
    logging.info("Temp table name created ...")
    return f"{config['project']}.{config['dataset']}.{prefix}_{config['customer']}_{suffix}"


# ----------------------------------------------------------------------------------------------------------------------
def get_bq_temp_table_def(config: tuple) -> bigquery.Table:
    try:
        tmp_table_def = bigquery.Table(config[0])
        tmp_table_def.expires = datetime.datetime.now(pytz.utc) + datetime.timedelta(minutes=config[2]["expiration"])
        tmp_table_def.schema = config[1]
        logging.info("BigQuery table structure created ...")
    except NameError:
        logging.error("Error trying to create bq table structure: %s", NameError)

    return tmp_table_def


# ----------------------------------------------------------------------------------------------------------------------
def create_bq_tmp_table(client: bigquery.Client, tmp_table: bigquery.Table):
    try:
        bq_client = client()
        bq_client.create_table(tmp_table)
        logging.info("BigQuery temp table has created")
    except NameError:
        logging.error("Error trying to create bq temp table: %s", NameError)


# ----------------------------------------------------------------------------------------------------------------------
def get_last_avro_filename_from_bucket(config: dict):
    try:
        client = storage.Client()
        bucket = client.get_bucket(config['bucket'])
        dates = []
        blobs = client.list_blobs(bucket, prefix='requests/', delimiter='/')

        for blob in blobs:
            n = blob.name
            if n.endswith(".avro"):
                date_name = dt.strptime(str(n[9:-5]), '%Y-%m-%dT%H:%M:%S.%fz')
                dates.append(date_name)

        final_date = str(sorted(dates, reverse=True)[0])[0:-3]
        logging.info("Last avro filename obtained...")
    except NameError:
        logging.error("Error trying to get last avro file name from bucket: %s", NameError)

    return final_date[0:10] + 'T' + final_date[11:] + 'Z.avro'


# ----------------------------------------------------------------------------------------------------------------------
def job_avro_load_to_bq_tmp_table(client: bigquery.Client,
                                  temp_table_name: str,
                                  file_path: str,
                                  file_name: str,
                                  ):
    try:
        bq_client = client()
        job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.AVRO)
        uri = file_path + file_name
        load_job = bq_client.load_table_from_uri(uri,
                                                 temp_table_name,
                                                 job_config=job_config)
        logging.info("Loading data ...")
        load_job.result()
        logging.info(f"Data file avro has been loaded to BigQuery (job status {load_job.state}) ...")
    except NameError:
        logging.error("Error trying to load data from avro to bigquery: %s", NameError)


# ----------------------------------------------------------------------------------------------------------------------
def get_query_context(context: str, src: str):
    query = json.loads(open('./process/query.json', 'r').read())
    return f"""{query[context][0][src]}"""


# ----------------------------------------------------------------------------------------------------------------------
def query_heineken_upsert(tmp_table_name: str) -> str:
    return get_query_context(context='bigquery', src='merge_heineken_temp_table').replace(
        '<TEMP_TABLE>', tmp_table_name)


# ----------------------------------------------------------------------------------------------------------------------
def query_erp_upsert():
    return get_query_context(context='bigquery', src='merge_external_query_erp')


# ----------------------------------------------------------------------------------------------------------------------
def get_config():
    params = json.loads(open('./process/params.json', 'r').read())
    return params["config"][0]


# ----------------------------------------------------------------------------------------------------------------------
def bq_exec_query(client: bigquery.Client, query: str, src: str):
    try:
        bq_client = client()
        query_job = bq_client.query(query)
        query_job.result()
        logging.info(f"Query: {src} executed with num_dml_affected_rows: %s", query_job.num_dml_affected_rows)
    except NameError:
        logging.error(f"Error trying to execute: {src}")
