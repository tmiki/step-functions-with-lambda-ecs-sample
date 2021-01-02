import json

# import requests


def lambda_handler(event, context):
    """Sample Lambda function placed into a Step Function State Machine.

    Parameters
    ----------
    event: dict, required
    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    Custom Output Format: dict
        exit_code: int : This is like an exit code of the UNIX command.
        message: str : A message what you want tell us.
    """


    print(json.dumps(event))

    return {
        "exit_code": 0,
        "message": "This function has finished successfully.",
        "result_detail": {
            "return1": "returned_value1",
            "return2": "returned_value2"
        }
    }
