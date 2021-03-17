import logging

import azure.functions as func

from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings


def main(req: func.HttpRequest) -> func.HttpResponse:
    block_blob_service = BlockBlobService(account_name='teststorageazf', account_key='VTKjYr4cIq0J2QisKu/Mxag2A/YRlXicFbfGq/1TzLPdxw+RuDHzl1gBi1+ArFvk0fBuzYynGaLe21ubUuDJkQ==')
    # block_blob_service.create_container('containerupl')
    filebytes = block_blob_service.get_blob_to_bytes('containerupl','OutFilePy.csv')

    # logging.info(filebytes.content)
    
    return func.HttpResponse(filebytes.content, mimetype='application/bytes', status_code=200)
