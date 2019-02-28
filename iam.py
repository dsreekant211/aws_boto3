import boto3
import json
# role document
data = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
# creating instance profile
client = boto3.client('iam')
response = client.create_instance_profile(
    InstanceProfileName='ec2-ssm-new',
    Path='/'
)


# creating iam role
client = boto3.client('iam')
response = client.create_role(
    Path='/',
    RoleName='ec2-ssm',
    AssumeRolePolicyDocument=json.dumps(data),
    Description='this is created from Boto3',
    Tags=[
        {
            'Key': 'Name',
            'Value': 'Lamb'
        },
    ]
)
# Add instance profile to role
response = client.add_role_to_instance_profile(
    InstanceProfileName='ec2-ssm-new',
    RoleName='ec2-ssm'
)
# Attaching s3 full access policy  to "lambda_s3" role
client = boto3.client('iam')
response = client.attach_role_policy(
    RoleName='ec2-ssm',
    PolicyArn="arn:aws:iam::aws:policy/AmazonSSMFullAccess"             
)
client = boto3.client('ec2')
response = client.associate_iam_instance_profile(
    IamInstanceProfile={
        'Arn': 'arn:aws:iam::185799809509:instance-profile/ec2-ssm-new',
        'Name': 'ec2-ssm'
    },
    InstanceId='i-0f016ee1bf031cda5'
)
