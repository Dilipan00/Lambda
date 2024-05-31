import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Define the number of days after which AMIs are considered old
    days_threshold = 30

    # Create EC2 client
    ec2 = boto3.client('ec2')

    # Describe all AMIs
    response = ec2.describe_images(Owners=['self'])

    # Iterate over AMIs
    for image in response['Images']:
        image_id = image['ImageId']
        creation_time = image['CreationDate']
        now = datetime.now()

        # Convert the creation time string to datetime object
        creation_time = datetime.strptime(creation_time, "%Y-%m-%dT%H:%M:%S.%fZ")

        # Calculate the age of the AMI in days
        age = (now - creation_time).days

        # Check if the AMI is old
        if age >= days_threshold:
            # Deregister AMI
            ec2.deregister_image(ImageId=image_id)
            print(f'Deregistered AMI: {image_id}')

            # Delete associated snapshots
            for block_device_mapping in image['BlockDeviceMappings']:
                if 'Ebs' in block_device_mapping:
                    snapshot_id = block_device_mapping['Ebs']['SnapshotId']
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f'Deleted snapshot: {snapshot_id}')
