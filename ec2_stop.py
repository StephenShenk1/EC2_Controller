import boto3

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='eu-west-2')  
    filters = [{
        'Name': 'tag:AutoManage',
        'Values': ['True']
    }]

    response = ec2.describe_instances(Filters=filters)
    instances_to_stop = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
        if instance['State']['Name'] == 'running'
    ]

    if instances_to_stop:
        print(f"Stopping instances: {instances_to_stop}")
        ec2.stop_instances(InstanceIds=instances_to_stop)
    else:
        print("No instances to stop.")

    return {
        'StoppedInstances': instances_to_stop
    }
