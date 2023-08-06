from .awssession import AWSSession


class AWSResource(AWSSession):

    def __init__(self, resource_name: str, access_key_id: str = None, secret_access_key: str = None, region: str = None):
        super().__init__(access_key_id, secret_access_key, region)
        self.__res = None
        self.__name = resource_name

    @property
    def resource(self):
        if self.__res is None:
            self.__res = self.session().client(self.__name)
        return self.__res
