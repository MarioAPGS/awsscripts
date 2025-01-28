import boto3

from models.Result import Result


def get_group(group_name: str) -> Result:
    iam_client = boto3.client('iam')

    # ARN de la política que deseas verificar
    result = Result()
    try:
        result.response = iam_client.get_group(GroupName=group_name)

    except Exception as e:
        result = Result(False, {}, str(e))

    finally:
        iam_client.close()
        return result

def create_group(account_id: str, name: str, policy_name_list: list[str]):
    #session = boto3.Session(profile_name="default")
    result = Result()
    try:
        iam_client = boto3.client('iam')

        result.response = iam_client.create_group(GroupName=name)

        for policy_name in policy_name_list:
            iam_client.attach_group_policy(
                GroupName=name,
                PolicyArn=f'arn:aws:iam::{account_id}:policy/{policy_name}'
            )

    except Exception as e:
        result = Result(False, {}, str(e))

    finally:
        iam_client.close()
        return result

def delete_group(name: str):
    iam_client = boto3.client('iam')

    result = Result()
    try:
        response = get_group(name).response
        users = response['Users']
        for user in users:
            user_name = user['UserName']
            iam_client.remove_user_from_group(
                GroupName=name,
                UserName=user_name
            )
        result.message = f"{len(users)} users detached. "

        response = iam_client.list_attached_group_policies(
            GroupName=name
        )
        for policy in response['AttachedPolicies']:
            iam_client.detach_group_policy(
                GroupName=name,
                PolicyArn=policy['PolicyArn']
            )
        result.response = iam_client.delete_group(GroupName=name)
        result.message += f"{len(response['AttachedPolicies'])} policies detached"

    except Exception as e:
        result = Result(False, {}, str(e))

    finally:
        iam_client.close()
        return result

