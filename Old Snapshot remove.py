import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Define the number of days after which snapshots are considered old
    days_threshold = 4

    # Create EC2 client
    ec2 = boto3.client('ec2')

    # Describe all snapshots
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Iterate over snapshots
    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        start_time = snapshot['StartTime']
        now = datetime.now()

        # Calculate the age of the snapshot in days
        age = (now - start_time.replace(tzinfo=None)).days

        # Check if the snapshot is old
        if age >= days_threshold:
            # Delete snapshot
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f'Deleted snapshot: {snapshot_id}')
