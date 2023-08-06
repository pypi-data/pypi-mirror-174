import boto3
from os import environ


class AWSSession:
    ACCESS_KEY = environ.get("AWS_ACCESS_KEY_ID")
    SECRET_KEY = environ.get("AWS_SECRET_ACCESS_KEY")
    REGION = environ.get("AWS_REGION")

    def __init__(self, access_key_id: str = None, secret_access_key: str = None, region: str = None):
        self.ACCESS_KEY = access_key_id
        self.SECRET_KEY = secret_access_key
        self.REGION = region
        self.__session = None

    def session(self):
        if self.__session is None:
            self.__session = boto3.session.Session(
                aws_access_key_id=self.ACCESS_KEY,
                aws_secret_access_key=self.SECRET_KEY,
                region_name=self.REGION
            )  # config=botocore.client.Config(max_pool_connections=50)
        return self.__session

    def set_session(self, session) -> 'any':
        self.__session = session
        return self

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass
