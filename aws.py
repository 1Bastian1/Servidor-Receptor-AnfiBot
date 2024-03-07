import boto3
import botocore
from botocore.exceptions import ClientError
import logging
import pandas as pd
from pandas import json_normalize
import os

# ODOO_USERNAME = os.environ['odoo_username']
# ODOO_PASSWORD = os.environ['odoo_password']
# ODOO_HOSTNAME = os.environ['odoo_hostname']
# ODOO_DATABASE = os.environ['odoo_database']
# BUCKET_NAME = os.environ['bucket_name_cencosud']
# TIME_LIMIT = float(os.environ['tiempo_limite_ejecucion'])
# DAY_LIMIT = int(os.environ['dias_limites_duracion_objs'])
AWS_SECRET= "OKfgOVjgcQGjMuMdYfbHtwkXnpcWWUPPJ725y811"
AWS_KEY = "AKIA3ANL6TU66VJC6RN3"


class Aws:
    def __init__(self):
        #self.s3_resource=boto3.resource('s3')
        
        self.s3_resource=boto3.resource('s3', aws_access_key_id=AWS_KEY,  aws_secret_access_key=AWS_SECRET)

    def upload_file(self,file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        s3_client = self.s3_resource.meta.client
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

