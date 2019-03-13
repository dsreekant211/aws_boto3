import boto3    
client = boto3.client('events')
response = client.put_rule(
    Name='run-command',
    ScheduleExpression='cron(26 12 * * ? *)',
    #EventPattern='string',
    State='ENABLED',
    Description='boto3',
    # RoleArn='string'
)
response = client.put_targets(
    Rule='run-command',
    Targets=[
        {
            'Id': '1234',
            'Arn': 'arn:aws:ssm:us-east-1::document/AWS-RunShellScript',
            'RoleArn': 'arn:aws:iam::185799809509:role/service-role/AWS_Events_Invoke_Run_Command_1248493732',
            'Input': '{"commands":["aws s3 ls"]}',	
            # 'InputTransformer': {
            #     'InputPathsMap': {
            #         "instance": "$.detail.instance","status": "$.detail.status"
            #     },
            #         'InputTemplate': '{"commands":["yum install htppd -y"]}'
            # },
            'RunCommandParameters': {
                    'RunCommandTargets': [
                        {
                            'Key': 'tag:Name',
                            'Values': [
                                'tomcat_dev'
                            ]
                        },
                    ]
                },
                
                
                
            },
        ]
        )  
        