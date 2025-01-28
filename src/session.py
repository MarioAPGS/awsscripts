import csv

import boto3


def config_session():
    profile="default"
    if not profile:
        return boto3
    else:
        return boto3.Session(profile_name=profile)

def session(credentials_path: str | None):
    if credentials_path == None or credentials_path == "":
        credentials_path = "../credentials/marioapgs_accessKeys.csv"

    with open(credentials_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            access_key_id = row['\ufeffAccess key ID']
            secret_access_key = row['Secret access key']

    # Configura la sesión de AWS
    return boto3.Session(
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    )

