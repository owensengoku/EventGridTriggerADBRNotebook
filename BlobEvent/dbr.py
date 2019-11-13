import json
import os
import requests
import logging

from json import JSONDecodeError

_DBR_TOKEN = os.getenv("DBR_TOKEN")
_DBR_WORKSPACE = os.getenv("DBR_WORKSPACE")
_DBR_JOB_ID = int(os.getenv("DBR_JOB_ID"))

def auth():
    return {"Authorization": f"Bearer {_DBR_TOKEN}"}

def run_job(blob_url) -> dict:
    job_url = _DBR_WORKSPACE + '/api/2.0/jobs/run-now'
    logging.info(job_url)
    payload = json.dumps({
        "job_id":_DBR_JOB_ID,
        "notebook_params":{
            "blob_url": blob_url
        }
    })
    logging.info(f"PAYLOAD TO DBR: {payload}")
    results = requests.post(
        url= job_url,
        data= payload,
        headers = auth()
    )
    try:
        output = results.json()
    except JSONDecodeError as je:
        logging.info(results.text)
        logging.info("Status code: {}".format(results.status_code))
        raise je

    return results.json()