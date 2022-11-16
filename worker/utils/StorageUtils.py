import os

from google.cloud import storage

from google.cloud.storage.blob import Blob
from env import BUCKET_NAME


class StorageUtils():

    @staticmethod
    def delete(file_name):
        """Deletes a blob from the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file_name)
        blob.delete()

        print(f"File {file_name} deleted.")

    @staticmethod
    def save(file_name, file):
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file_name).upload_from_string(file)
        print(f'Uploaded file: {bucket.blob(file_name).public_url}')


    @staticmethod
    def read(file_name):
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        return bucket.blob(file_name).download_as_bytes()