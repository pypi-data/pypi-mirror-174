import os.path

from google.cloud import storage
import traceback
import sys
from google.oauth2 import service_account
from .utils import *


class Handler(object):

    def bucket_exists(self, bucket_name: str) -> bool:
        pass

    def bucket_create(self, bucket_name: str) -> bool:
        pass

    def blob_find(self, bucket_name: str, blob_file_name: str) -> storage.blob.Blob | None:
        pass

    def blob_upload(self, onprem_file_path: str, bucket_name: str, blob_file_path: str, overwrite: bool = False):
        pass

    def blob_download(self, bucket_name: str, blob_file_path: str, local_path: str) -> int:
        pass

    def blob_set_metadata(self, bucket_name, blob_file_path, meta2update_input, mode='u'):
        pass

    def blob_change_storage_class(self, bucket_name: str, blob_file_path: str, new_storage_class: str) -> int:
        pass

    def blob_get_storage_class(self, bucket_name: str, blob_file_path: str) -> str | None:
        pass
