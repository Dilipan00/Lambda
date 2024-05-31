import boto3

def lambda_handler(event, context):
    # Specify the region where the security group exists
    region = 'your_region_name'
    
    # Specify the ID of the security group you want to delete
    security_group_id = 'your_security_group_id'
    
    # Create EC2 client
    ec2_client = boto3.client('ec2', region_name=region)
    
    try:
        # Describe the security group to retrieve its existing inbound rules
        response = ec2_client.describe_security_groups(GroupIds=[security_group_id])
        
        # Extract the inbound rules from the response
        inbound_rules = response['SecurityGroups'][0]['IpPermissions']
        
        # Check if any rule has the source set to "anywhere" (0.0.0.0/0)
        has_anywhere_rule = any({'CidrIp': '0.0.0.0/0'} in rule['IpRanges'] for rule in inbound_rules)
        
        if has_anywhere_rule:
            # Delete the security group
            ec2_client.delete_security_group(GroupId=security_group_id)
            
            return {
                'statusCode': 200,
                'body': 'Security group deleted successfully'
            }
        else:
            return {
                'statusCode': 200,
                'body': 'No security group rule with source "anywhere" found'
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }
