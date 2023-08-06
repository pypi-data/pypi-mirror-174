from .awsresource import AWSResource
from tempfile import gettempdir
import traceback
import logging
from io import TextIOWrapper
import os
import uuid


class AWSBucketFolderUpload:
    success: list = []
    error: list = []

    def __str__(self) -> str:
        return f"success: {self.success}, error: {self.error}"


class AWSBucketTempFile:

    @property
    def file_path(self) -> str:
        """
        Get the file path
        """
        return self._file_path
    
    @property
    def file_name(self) -> str:
        """
        Get the file name
        """
        return self._file_name

    @property
    def temp_dir(self) -> str:
        """
        Get the temporary directory
        """
        return self._temp_dir

    def __init__(self, data: bytes, temp_dir: str, file_name: str = None):
        self._temp_dir = temp_dir or gettempdir()
        self._file_name = file_name or str(uuid.uuid4())
        self._file_path = os.path.join(self.temp_dir, self.file_name)
        with open(self.file_path, 'wb') as fl:
            fl.write(data)
            fl.flush()

    def __enter__(self) -> 'AWSBucketTempFile':
        return self

    def open(self, open_mode: str = None) -> TextIOWrapper:
        """
        Open the file in the specified mode

        Parameters:
            open_mode (str): File open mode
        """
        return open(self.file_path, open_mode or 'rb')

    def __exit__(self, *_):
        os.remove(self.file_path)


class AWSBucket(AWSResource):

    def __init__(self, bucket_name: str, access_key_id: str = None, secret_access_key: str = None, region: str = None):
        super().__init__('s3', access_key_id, secret_access_key, region)
        self.bucket_name = bucket_name

    def get_object(self, key: str) -> bytes:
        """
        Get a file in bytes

        Parameters:
            key (str): Bucked file path
        """
        resp = self.resource.get_object(Bucket=self.bucket_name, Key=key)
        if resp['ResponseMetadata']['HTTPStatusCode'] == 200:
            return resp['Body'].read()
        raise FileNotFoundError(
            f"Error getting object from bucket {self.bucket_name} with key {key}")

    def put_object(self, file_bytes: bytes, key: str) -> None:
        """
        Put a file in bytes

        Parameters:
            file_bytes: bytes
            key (str): Bucked file path
        """
        self.resource.put_object(
            Body=file_bytes, Bucket=self.bucket_name, Key=key)

    def open_temp(self, key: str, temp_dir: str = None, file_name: str = None) -> AWSBucketTempFile:
        """
        Save the file locally and delete it when closed

        Parameters:
            key (str): Bucked file path
            temp_dir (str): Local temp folder path
            file_name (str): Local file name
        """
        data_arr = self.get_object(key)
        return AWSBucketTempFile(data_arr, temp_dir=temp_dir, file_name=file_name)

    def download(self, key: str, output_file_path: str) -> None:
        """
        Download a file

        Parameters:
            key (str): Bucked file path
            output_file_path (str): Local file path
        """
        with open(output_file_path, 'wb') as fl:
            self.resource.download_fileobj(self.bucket_name, key, fl)

    def upload(self, file_path: str, key: str) -> None:
        """
        Upload a file

        Parameters:
            file_path (str): Local file path
            key (str): Bucked file path
        """
        self.resource.upload_file(file_path, self.bucket_name, key)

    def exists(self, key: str) -> bool:
        """
        If a file exists

        Returns:
            bool: True if exists
        """
        try:
            self.resource.head_object(Bucket=self.bucket_name, Key=key)
            return True
        except Exception:
            return False

    def upload_folder(self, local_path_folder: str, dst_prefix: str, re_write: bool = False) -> AWSBucketFolderUpload:
        """
        Upload all file from a folder
        """
        result = AWSBucketFolderUpload()
        for name in os.listdir(local_path_folder):
            npath = os.path.join(local_path_folder, name)
            if os.path.isfile(npath):
                dst_filepath = os.path.join(dst_prefix, name)
                if re_write or not self.exists(dst_filepath):
                    logging.info(f"Uploading {npath} to {dst_filepath}")
                    try:
                        self.upload(npath, dst_filepath)
                    except Exception as ex:
                        traceback.print_exc()
                        result.error.append(npath)
                        raise ex
                    else:
                        result.success.append(npath)
                else:
                    logging.warning(
                        f"{npath} already exists in {os.path.join(self.bucket_name, dst_prefix)}")
            else:
                resp = self.upload_folder(
                    npath, os.path.join(dst_prefix, name))
                result.success.extend(resp.success)
                result.error.extend(resp.error)
        return result


if __name__ == '__main__':
    AWSBucket('test').exists('test.txt')
