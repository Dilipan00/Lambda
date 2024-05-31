import boto3
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    filters = [{
         'Name': 'tag:state:scheduleName',
         'Values': ['24x7']
       }]

    #get all instances   
    AllInstances=[instance.id for instance in ec2.instances.all()]
    # get instances with that tag and value
    instances = ec2.instances.filter(Filters=filters)

    RunningInstancesWithTag = [instance.id for instance in instances]

    RunningInstancesWithoutTag= [x for x in AllInstances if x not in  RunningInstancesWithTag]

    if len(RunningInstancesWithoutTag) > 0:
            print("found instances with out tag")
            ec2.instances.filter(InstanceIds = RunningInstancesWithoutTag).stop() #for stopping an ec2 instance
            print("instance stopped")
    else:
        print("let it be run as tag value is 24*7")