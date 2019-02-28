# Print out bucket names
import boto3
ec2 = boto3.resource('ec2')
instance = ec2.create_instances(
    
    ImageId='ami-035be7bafff33b6b6',
    InstanceType='t2.micro',
    MinCount=1,
    MaxCount=1,
    KeyName='testing',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'myinstance'
                },
            ]
        },
    ],
)
    
 
   #ResourceType': 'client-vpn-endpoint'|'customer-gateway'|'dedicated-host'|'dhcp-options'|'elastic-ip'|'fleet'|'fpga-image'|'image'|'instance'|'internet-gateway'|'launch-template'|'natgateway'|'network-acl'|'network-interface'|'reserved-instances'|'route-table'|'security-group'|'snapshot'|'spot-instances-request'|'subnet'|'transit-gateway'|'transit-gateway-attachment'|'transit-gateway-route-table'|'volume'|'vpc'|'vpc-peering-connection'|'vpn-connection'|'vpn-gateway',

    
    
 