import copy
import sys
import os
import boto3
from datetime import datetime
import traceback
from .utils import *
import re


class S3ConnectInfo(object):
    access_key_id = None
    secret_access_key = None

    def __init__(self, access_key_id: str, secret_access_key: str):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key


class HandlerS3(object):

    def bucket_exists(self, bucket_name: str) -> bool:
        pass

    def bucket_create(self, bucket_name: str, region: str = '') -> bool:
        pass

    def file_find(self, bucket_name: str, s3_file_path: str) -> Union[dict, None]:
        pass

    def file_upload(self, onprem_file_path: str, bucket_name: str, s3_file_path: str, overwrite: bool = False) -> int:
        pass

    def file_download(self, bucket_name: str, s3_file_path: str, local_path: str) -> int:
        pass

    def file_set_tag(self, bucket_name: str, s3_file_path: str, data_dict2update_in: dict, mode: str = 'u') -> int:
        pass

    def file_set_metadata(self, bucket_name, s3_file_path, meta2update_input, mode='u'):
        pass

    def file_change_storage_class(self, bucket_name, s3_file_path, new_storage_class):
        pass

    def file_send_restore_request(self, bucket_name, s3_file_path, operation_tier):
        pass

    def file_restore_ongoing(self, bucket_name, s3_file_path) -> bool:
        pass

    def file_get_storage_class_archive_status(self, bucket_name, s3_file_path):
        pass
