import boto3


client = boto3.client('ssm')
response = client.send_command(
    InstanceIds=[
            'i-0f016ee1bf031cda5',
    ],    
    DocumentName='AWS-RunShellScript',
    DocumentVersion='1',
    Comment='to install httpd using AWS SSM',
    Parameters={
        'commands': [
            'yum install httpd -y',
            'service httpd start'
        ]
    },
)