from setup_bucket import configure_bucket_permission


def lambda_handler():
    bucket_name = 'imelios'
    account_id = '222927973491'
    configure_bucket_permission(bucket_name, account_id)
    return {
            'statusCode': 200,
            'body': 'Ok'
        }

lambda_handler()
