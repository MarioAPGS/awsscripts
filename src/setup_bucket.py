import boto3

from iam_groups import create_group, delete_group, get_group
from iam_policy import create_policy, delete_policy, get_policy


def get_bucket_read_policy(bucket_name: str) -> dict:
    return {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    f"arn:aws:s3:::{bucket_name}",
                    f"arn:aws:s3:::{bucket_name}/*"
                ]
            }
        ]
    }

def get_bucket_write_policy(bucket_name: str) -> dict:
    return {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:PutObject",
            "Resource": f"arn:aws:s3:::{bucket_name}/*"
        }
    ]
}

def get_bucket_delete_policy(bucket_name: str) -> dict:
    return {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:DeleteObject",
                "s3:ListMultipartUploadParts",
                "s3:AbortMultipartUpload"
            ],
            "Resource": [
                f"arn:aws:s3:::{bucket_name}",
                f"arn:aws:s3:::{bucket_name}/*"
            ]
        }
    ]
}

def configure_bucket_permission(bucket_name: str, account_id: str):
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    if bucket_name in buckets:
        # S3 Read policy
        if not get_policy(account_id, f"S3{bucket_name}R").success:
            output = create_policy(f"S3{bucket_name}R", f"readonly on the bucket {bucket_name}", policy=get_bucket_read_policy(bucket_name))
            print(output.success, f"Create policy: S3{bucket_name}R")
        else:
            print(f"policy S3{bucket_name}R already exists")

        # S3 Write policy
        if not get_policy(account_id, f"S3{bucket_name}W").success:
            output = create_policy(f"S3{bucket_name}W", f"write on the bucket {bucket_name}", policy=get_bucket_write_policy(bucket_name))
            print(output.success, f"Create policy: S3{bucket_name}W")
        else:
            print(f"policy S3{bucket_name}W already exists")

        # S3 Delete policy
        if not get_policy(account_id, f"S3{bucket_name}D").success:
            output = create_policy(f"S3{bucket_name}D", f"delete on the bucket {bucket_name}", policy=get_bucket_delete_policy(bucket_name))
            print(output.success, f"Create policy: S3{bucket_name}D")
        else:
            print(f"policy S3{bucket_name}D already exists")

        # S3 RW group
        if not get_group(f"S3_{bucket_name}_RW").success:
            response = create_group(account_id, f"S3_{bucket_name}_RW", [f"S3{bucket_name}R", f"S3{bucket_name}W"])
            print(response.success, f"Create group: S3_{bucket_name}_RW")
        else:
            print(f"group S3{bucket_name}_RW already exists")

        # S3 RWD group
        if not get_group(f"S3_{bucket_name}_RWD").success:
            response = create_group(account_id, f"S3_{bucket_name}_RWD", [f"S3{bucket_name}R", f"S3{bucket_name}W", f"S3{bucket_name}D"])
            print(response.success, f"Create group: S3_{bucket_name}_RWD")
        else:
            print(f"group S3{bucket_name}_RWD already exists")


def delete_bucket_permission(bucket_name: str, account_id: str):
    if get_group(f"S3_{bucket_name}_RW").success:
        response = delete_group(f"S3_{bucket_name}_RW")
        print(response.success, f"Delete group: S3_{bucket_name}_RW")
        print(response.message)

    if get_group(f"S3_{bucket_name}_RWD").success:
        response = delete_group(f"S3_{bucket_name}_RWD")
        print(response.success, f"Delete group: S3_{bucket_name}_RWD")
        print(response.message)

    if get_policy(account_id, f"S3{bucket_name}R").success:
        output = delete_policy(account_id, f"S3{bucket_name}R")
        print(output.success, f"Delete policy: S3{bucket_name}R")

    if get_policy(account_id, f"S3{bucket_name}W").success:
        output = delete_policy(account_id, f"S3{bucket_name}W")
        print(output.success, f"Delete policy: S3{bucket_name}W")

    if get_policy(account_id, f"S3{bucket_name}D").success:
        output = delete_policy(account_id, f"S3{bucket_name}D")
        print(output.success, f"Delete policy: S3{bucket_name}D")
