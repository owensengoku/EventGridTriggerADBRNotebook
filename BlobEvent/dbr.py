import os
import requests


_DBR_TOKEN = os.getenv("DBR_TOKEN")
_DBR_WORKSPACE = os.getenv("DBR_TOKEN")
_DBR_JOB_ID = int(os.getenv("DBR_JOB_ID"))

def auth():
    return {"Authorization": f"Bearer {_DBR_TOKEN}"}

def run_job(blob_url):
    job_url = _DBR_WORKSPACE + '/api/2.0/jobs/run-now'
    payload = {
        "job_id":_DBR_JOB_ID,
        "notebook_params":{
            "blob_url": blob_url
        }
    }
    results = requests.post(
        url= job_url,
        data= payload,
        headers = auth()
    )

    return results.json()