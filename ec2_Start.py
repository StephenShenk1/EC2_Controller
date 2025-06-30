import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='eu-west-2')  # Change region as needed

    # Filter EC2 instances with tag Schedule=Start
    filters = [{
        'Name': 'tag:AutoManage',
        'Values': ['True']
    }]

    # Get instances that are currently stopped
    response = ec2.describe_instances(Filters=filters)
    instances_to_start = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
        if instance['State']['Name'] == 'stopped'
    ]

    # Start the instances
    if instances_to_start:
        print(f"Starting instances: {instances_to_start}")
        ec2.start_instances(InstanceIds=instances_to_start)
    else:
        print("No instances to start.")

    return {
        'StartedInstances': instances_to_start
    }
