from json import dumps
from .awsresource import AWSResource


class AWSLambda(AWSResource):
    """
    Logic for invoke lambda function
    """

    def __init__(self, function_name, access_key_id: str = None, secret_access_key: str = None, region: str = None):
        super().__init__('lambda', access_key_id, secret_access_key, region)
        self.__function_name = function_name

    def invoke(self, payload: dict) -> dict:
        return self.resource.invoke(
            FunctionName=self.__function_name,
            InvocationType='Event',
            Payload=dumps(payload)
        )


if __name__ == '__main__':
    AWSLambda('function').invoke({
        "channel": "channel",
        "type_message": "error",
        "message": "An error has occurred"
    })
