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


    print("event: " + json.dumps(event))
    print(event)

    if (event['WillSucceed'] == True):
        print("This function has succeeded.")
        return {
            "exit_code": 0,
            "message": "This function has succeeded."
        }
    else:
        print("This function has failed.")
        return {
            "exit_code": 9,
            "message": "This function has failed.",
            "cause_of_failure": {
                "cause1": "reason1",
                "cause2": "reason2"
            }
        }


