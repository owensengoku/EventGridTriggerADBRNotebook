# Using Azure Functions to Trigger a Databricks Notebook

In this sample, we take an Event Grid Trigger function that watches for a blob (Gen 2) storage event (Creation of a blob) and then triggers a databricks notebook and passes the blob's URL to the notebook as a WASBS:// path.

## Instructions

1. Install [VS Code](https://code.visualstudio.com/)
1. Install [Python 3.6.8](https://www.python.org/downloads/release/python-368/)
1. Install the [Python Extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
1. Install the [Azure Functions Extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)
1. Follow the steps in this [quickstart tutorial](https://docs.microsoft.com/en-us/azure/python/tutorial-vs-code-serverless-python-01) to verify your installations.
1. Create a [Databricks Notebook](https://docs.azuredatabricks.net/jobs.html#create-a-job) job and save the Job ID for steps below.
1. Create a [Personal Access Token](https://docs.azuredatabricks.net/dev-tools/api/latest/authentication.html#generate-a-token) in Databricks and save the PAT for the step below.
1. Clone this repository to your local machine.
1. Create a local.settings.json in the root of your folder with the following settings
    ```
    {
    "IsEncrypted": false,
    "Values": {
        "AzureWebJobsStorage": "UseDevelopmentStorage=true",
        "FUNCTIONS_WORKER_RUNTIME": "python",
        "DBR_TOKEN": "<DATABRICKS PERSONAL ACCESS TOKEN>",
        "DBR_WORKSPACE": "https://<YOUR DATABRICKS REGION>.azuredatabricks.net",
        "DBR_JOB_ID": "<JOB NUMBER>"
    }
    }
    ```
1. [Deploy the Azure Function](https://docs.microsoft.com/en-us/azure/python/tutorial-vs-code-serverless-python-05)
   * You may have to select the advanced mode to control which resource group the function is deployed to.
1. From the portal, [create an Event Grid Subscription](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-event-grid#create-a-subscription) that watches your Storage Account.
   * Event Schema: Event Grid Schema
   * Topic Types: Storage Account
   * Subscription, Resource Group, Resource: Choose the location of the storage account you want to watch.
   * Filter to Event Types: Choose only Blob Created
   * Endpoint Details should be automatically filled in to your deployed Azure Function.
1. Test your function by adding a file to the storage account.  You should be able to see logs of the [events in Event Grid](https://docs.microsoft.com/en-us/azure/event-grid/monitor-event-delivery) and get [logs of your function](https://docs.microsoft.com/en-us/azure/azure-functions/functions-monitoring).

## Known Issues

* Currently, this project is designed to run for a single JOB ID and could be further enhanced to look up the correct JOB ID from Azure Table Storage given the file path of the blob.