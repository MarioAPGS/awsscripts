import boto3
from models.Result import Result


def clean_acl_by_name(acl_name: str)  -> Result:
    ec2_client = boto3.client('ec2')
    result = Result()

    try:
        response = ec2_client.describe_network_acls(Filters=[{'Name': 'tag:Name', 'Values': [acl_name]}])

        if 'NetworkAcls' not in response or not response['NetworkAcls']:
            print(f"ACL group '{acl_name}' does not exist.")
            return
        result = clean_acl_by_object(response['NetworkAcls'][0])
        
    except Exception as e:
        result = Result(False, {}, str(e))

    finally:
        ec2_client.close()
        return result


def clean_acl_by_object(acl) -> Result: 
    ec2_client = boto3.client('ec2')
    result = Result()

    try:
        acl_id = acl['NetworkAclId']
        entries = list(filter(lambda x: (x['RuleNumber'] >= 1 and x['RuleNumber'] <= 32766), acl['Entries']))
        
        count = 0
        print(f"Cleaning {len(entries)} entries")
        for entry in entries:
            count += 1
            ec2_client.delete_network_acl_entry(
                Egress=entry['Egress'],
                NetworkAclId=acl_id,
                RuleNumber=entry['RuleNumber']
            )
            print(f"{count}/{len(entries)}")
        result = Result(True, {"entries": entries}, f"{len(entries)} entries deleted")

    except Exception as e:
        result = Result(False, {}, str(e))

    finally:
        ec2_client.close()
        return result
    


def add_acls(acl_name: str, ip_ranges: list[str]) -> Result:
    
    ec2_client = boto3.client('ec2')
    result = Result()
    result.response = {"errors": {}}
    isAnyError = False
    try:
        response = ec2_client.describe_network_acls(Filters=[{'Name': 'tag:Name', 'Values': [acl_name]}])

        if 'NetworkAcls' not in response or not response['NetworkAcls']:
            return Result(False, {}, f"ACL group '{acl_name}' does not exist.")
        
        clean_result = clean_acl_by_object(response['NetworkAcls'][0])
        if not clean_result.success:
            return clean_result
        
        acl_id = response['NetworkAcls'][0]['NetworkAclId']

        start=100
        for i, range in enumerate(ip_ranges):
            try:
                ipInfo = range.split(":")
                portsInfo = None
                if len(ipInfo) == 2:
                    portsInfo = {'From': int(ipInfo[1]), 'To': int(ipInfo[1])}
                if len(ipInfo) == 3:
                    portsInfo = {'From': int(ipInfo[1]), 'To': int(ipInfo[2])}

                ec2_client.create_network_acl_entry(
                    NetworkAclId=acl_id,
                    RuleNumber=start+(i*2),
                    Protocol='6',
                    RuleAction='allow',
                    Egress=False,
                    CidrBlock=ipInfo[0],
                    PortRange=portsInfo
                )
                print(f"[{i+1}/{len(ip_ranges)}] Range added.")
            except Exception as e:
                isAnyError = True
                result.response["errors"][range] = str(e)
                print(f"[{i+1}/{len(ip_ranges)}] Error {range}: {str(e)}")
        result = Result(not isAnyError, result.response, "")

    except Exception as e:
        result = Result(False, {}, str(e))

    finally:
        ec2_client.close()
        return result
