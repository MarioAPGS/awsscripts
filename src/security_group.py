import boto3
from models.Result import Result

def change_security_groups(instance_id: str, security_group_id: list[str]) -> Result:
    ec2_client = boto3.client('ec2')

    # ARN de la política que deseas verificar
    result = Result()
    try:
        result.response = ec2_client.modify_instance(
        instance_id=instance_id,
        security_group_ids=security_group_id
        )
        
    except Exception as e:
        result = Result(False, {}, str(e))

    finally:
        ec2_client.close()
        return result

def clear_security_group_by_id(security_group_id: str) -> Result:
    ec2_client = boto3.client('ec2')
    isAnyError = False
    errors = {"errors":{}}
    
    # Obtiene las reglas de entrada actuales
    response_ingress = ec2_client.describe_security_group_rules(
        Filters=[
            {
                'Name': 'group-id',
                'Values': [security_group_id],
            },
        ],
    )

    for rule in response_ingress['SecurityGroupRules']:
        if not rule["IsEgress"]:
            try:
                ec2_client.revoke_security_group_ingress(
                    GroupId=security_group_id,
                    SecurityGroupRuleIds=[rule['SecurityGroupRuleId']]
                )
            
            except Exception as e:
                isAnyError = True
                errors[rule["CidrIpv4"]] = str(e)
                print(f"[ERROR] {str(rule)} => {str(e)}")

    ec2_client.close()
    return Result(not isAnyError, errors, "")

def get_security_group(group_name: str, description: str = "", vpc_id: str = "", create: bool = False) -> Result:
    ec2_client = boto3.client('ec2')

    result = Result()
    try:
        response = ec2_client.describe_security_groups(
        Filters=[
            {'Name': 'group-name', 'Values': [group_name]}
        ]
        )

        if response['SecurityGroups']:
            result = Result(True, response['SecurityGroups'][0], "OK")
        elif create:
            new_group = ec2_client.create_security_group(
                GroupName=group_name,
                Description=description,
                VpcId=vpc_id
            )
            result = Result(True, new_group, "Group created")
        else:
            result = Result(True, {}, "No results")
        
    except Exception as e:
        result = Result(False, {}, str(e))

    finally:
        ec2_client.close()
        return result
    
    

def add_security_group_entry_rules_by_id(security_group_id: str, ips: list[str]) -> Result: 
    ec2_client = boto3.client('ec2')
    isAnyError = False
    errors = {"errors": {}}
    clear_response = clear_security_group_by_id(security_group_id)
    if clear_response.success:
        for ip in ips:
            try:
                ec2_client.authorize_security_group_ingress(
                    GroupId=security_group_id,
                    IpPermissions=[
                        {
                            'IpProtocol': '-1',
                            #'FromPort': 80,  # Puerto que deseas permitir
                            #'ToPort': 80,
                            'IpRanges': [{'CidrIp': ip}],
                        },
                    ]
                )
                print(f"[OK] {ip}")
                
            except Exception as e:
                isAnyError = True
                errors["errors"][ip] = str(e)
                print(f"[ERROR] {ip} => {str(e)}")

        ec2_client.close()
        return Result(not isAnyError, errors, "")
    else:
        return clear_response
    

def add_security_group_entry_rules_by_name(group_name: str, ips: list[str], description: str = "", vpc_id: str = "", create: bool = False) -> Result:

    security_group_request = get_security_group(group_name, description, vpc_id, create)
    if security_group_request.success:
        group_id = security_group_request.response['GroupId']
        return add_security_group_entry_rules_by_id(group_id, ips)
    else:
        return security_group_request