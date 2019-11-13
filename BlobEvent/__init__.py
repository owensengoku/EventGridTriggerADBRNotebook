import json
import logging

from .dbr import run_job

import azure.functions as func

def main(event: func.EventGridEvent):
    result = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    })

    logging.info('Python EventGrid trigger received an event: %s', result)

    blob_url = event.get_json().get("url")
    if blob_url is None:
        logging.info(f"{event.id} did not contain a 'url' attribute in its 'data' attribute.  Exiting.")
        exit(1)
    
    # Reshape the blob url to be wasbs format (wasbs://CONTAINER@STORAGE_ACCOUNT/FILE_PATH)
    # Input as https://STORAGE_ACCOUNT/CONTAINER/FILE_PATH
    slashes_pos = blob_url.index('://') + 3
    end_storage_acct_pos = blob_url[(slashes_pos):].index('/') + slashes_pos
    end_container_pos = blob_url[(end_storage_acct_pos+1):].index('/')+end_storage_acct_pos+1

    storage_acct = blob_url[slashes_pos:end_storage_acct_pos]
    container = blob_url[(end_storage_acct_pos+1):end_container_pos]
    filepath = blob_url[(end_container_pos+1):]

    wasbs_url = f"wasbs://{container}@{storage_acct}/{filepath}"
    logging.info(f"Running a job for this wasbs file: {wasbs_url}")
    job_results = run_job(wasbs_url)
    job_string = json.dumps(job_results)

    logging.info(f"Job trigger results were: {job_results}")
    logging.info(f"Completed Event Grid Trigger for {event.id}")


    
