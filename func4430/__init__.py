import logging

import azure.functions as func

from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings


def main(req: func.HttpRequest) -> func.HttpResponse:
    block_blob_service = BlockBlobService(account_name='teststorageazf', account_key='VTKjYr4cIq0J2QisKu/Mxag2A/YRlXicFbfGq/1TzLPdxw+RuDHzl1gBi1+ArFvk0fBuzYynGaLe21ubUuDJkQ==')
    # block_blob_service.create_container('containerupl')

    logging.info("files list here is ")
    logging.info(req.files['test1'])

    block_blob_service.create_blob_from_stream('containerupl', 'OutFilePy.csv', req.files['test1'])

    generator = block_blob_service.list_blobs('containerupl')
    for blob in generator:
        logging.info(blob.name)
    
    return func.HttpResponse(
    "uploaded sucessfully",
    status_code=200)
