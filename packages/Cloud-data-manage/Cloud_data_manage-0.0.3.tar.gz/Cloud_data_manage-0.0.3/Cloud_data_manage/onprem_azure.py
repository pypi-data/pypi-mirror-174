import os
import sys
from datetime import datetime
import azure.core.exceptions
from .utils import *
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobProperties
from azure.storage.blob import ContainerClient
from azure.storage.blob import ContentSettings
from azure.identity import ClientSecretCredential
import copy
import traceback


class ServicePrincipal(object):
    tenant_id = None
    client_id = None
    client_secret = None
    auth_url = None

    def __init__(self, tenant_id: str, client_id: str, client_secret: str, auth_url: str):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url


class ConnectionString(object):
    connection_string = None

    def __init__(self, connection_string: str):
        self.connection_string = connection_string


class StorageAccountSAS(object):
    sas_url = None

    def __init__(self, sas_url: str):
        self.sas_url = sas_url


class HandlerStorageAccount(object):

    def container_exists(self, container_name: str) -> bool:
        pass

    def container_create(self, container_name: str) -> bool:
        pass

    def blob_find(self, container_name: str, blob_file_path: str) -> Union[BlobProperties, None]:
        pass

    def blob_upload(self, container_name: str, onprem_file_path: str,
                    blob_file_path: str, overwrite: bool = False) -> int:
        pass

    def blob_download(self, container_name: str, blob_file_path: str, local_path: str) -> int:
        pass

    def blob_set_tag(self, container_name: str, blob_file_path: str, data_dict2update: dict, mode: str = 'u') -> int:
        pass

    def blob_set_metadata(self, container_name: str, blob_file_path: str,
                          meta2update_dict: dict, mode: str = 'u') -> int:
        pass

    def blob_send_change_tier_request(self, container_name: str, new_tier: str, blob_file_path: str) -> int:
        pass

    def blob_get_tier(self, container_name: str, blob_file_path: str) -> str | None:
        pass


class ContainerSAS(object):
    blob_sas_url = None

    def __init__(self, blob_sas_url: str):
        self.blob_sas_url = blob_sas_url


class ServiceClientAndContainerName(object):
    blob_service_client = None
    container_name = None

    def __init__(self, blob_service_client: BlobServiceClient, container_name: str):
        self.blob_service_client = blob_service_client
        self.container_name = container_name


class HandlerContainer(object):

    def blob_find(self, blob_file_path: str) -> Union[BlobProperties, None]:
        pass

    def blob_upload(self, onprem_file_path: str, blob_file_path: str, overwrite: bool = False) -> int:
        pass

    def blob_download(self, blob_file_path: str, local_path: str) -> int:
        pass

    def blob_set_metadata(self, blob_file_path: str, meta2update_dict_in: dict, mode: str = 'u') -> int:
        pass

    def blob_send_change_tier_request(self, new_tier: str, blob_file_path: str) -> int:
        pass

    def blob_get_tier(self, blob_file_path: str) -> str | None:
        pass
