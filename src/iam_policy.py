import json
import boto3
from session import session
from models.Result import Result

def get_policy(account_id: str, policy_name: str) -> Result:
    iam_client = boto3.client('iam')

    # ARN de la política que deseas verificar
    result = Result()
    try:
        result.response = iam_client.get_policy(PolicyArn=f'arn:aws:iam::{account_id}:policy/{policy_name}')
        
    except Exception as e:
        result = Result(False, {}, str(e))

    finally:
        iam_client.close()
        return result


def create_policy(name: str, description: str, policy: dict) -> Result:
    #session = boto3.Session(profile_name="default")
    iam_client = boto3.client('iam')

    policy_document_json = json.dumps(policy)
    result = Result()
    try:
        result.response = iam_client.create_policy(
            PolicyName=name,
            PolicyDocument=policy_document_json,
            Description=description
        )

    except Exception as e:
        result = Result(False, {}, str(e))

    finally:
        iam_client.close()
        return result

def delete_policy(account_id: str, policy_name: str) -> Result:
    iam_client = boto3.client('iam')
    result = Result()
    try:
        result.response = iam_client.delete_policy(PolicyArn=f'arn:aws:iam::{account_id}:policy/' + policy_name)

    except Exception as e:
        result = Result(False, {}, str(e))

    finally:
        iam_client.close()
        return result
