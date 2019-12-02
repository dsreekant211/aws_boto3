import json
from datetime import datetime

import boto3
import numpy as np
import pandas as pd
import xlsxwriter
from bson import json_util

writer = pd.ExcelWriter('windows1.xlsx', engine='xlsxwriter')

def datetime_handler(x):
    '''
    :Handles the datime formatting error
    '''
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

def get_all_instances():
    '''
    :Get All Instances
    '''
    client = boto3.client('ec2',verify=False)
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running',
                ]
            },
            {
                'Name': 'platform',
                'Values':['windows']
            },
            {
               'Name': 'private-ip-address',
               'Values': [ "10.235.200.163",]
            },
            # {
            #     'Name': 'tag-key',
            #     'Values': ['Elsevier_Metrics']
            # }
            # {
            #     'Name': 'ip-address',
            #     'Values': ['18.140.186.61',]
            # }
        ],
        DryRun=False,
        MaxResults=123,
    )
    return response

#Metrics Data into excel
def get_metrices(data):
    '''
    :Get metrics and form an excel
    '''
    client = boto3.client('cloudwatch',verify=False)
    data = list (data['Reservations'])
    #print (data[0]['Instances'])
    
    for i in data:        
        instance_id = i['Instances'][0]['InstanceId']
        image_id = i['Instances'][0]['ImageId']
        instance_type = i['Instances'][0]['InstanceType']
        
        for t in i['Instances'][0]['Tags']:
            if t['Key'] == "Name":
                name = t['Value']

        response = client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': instance_id
                },
            ],
            StartTime=datetime(2019,11,25),
            EndTime=datetime(2019,12,2),
            Period=3600 ,
            Statistics=[
                'Average','Minimum','Maximum',
                # 'Minimum','Maximum',

            ],
            Unit='Percent'            
        )
        
        
        response_mem_win = client.get_metric_statistics(
            Namespace='CWAgent',
            MetricName='Memory % Committed Bytes In Use',
            Dimensions=[
                 {
                    'Name': 'InstanceId',
                    'Value': instance_id
                },
                {
                    'Name': "ImageId",
                    'Value': image_id
                },
                {
                    'Name': "InstanceType",
                    'Value': instance_type
                },
                {
                    "Name": "objectname",
                    "Value": "Memory"
                },
            ],
            StartTime=datetime(2019,11,25),
            EndTime=datetime(2019,12,2),
            Period=3600 ,
            Statistics=[
                'Average','Minimum','Maximum',
                # 'Minimum','Maximum',
            ],
            Unit='None'
        ) 
             
        
        if response:
            sorted_data = sorted(response['Datapoints'], key=lambda x: datetime.strptime(str(x['Timestamp']), '%Y-%m-%d  %H:%M:%S%z'))
            response['Datapoints'] = sorted_data
            json_data = json.dumps(response["Datapoints"], default=datetime_handler)
            df1 = pd.DataFrame(eval(json_data))
            df1.fillna('', inplace=True)
            df1["C"] = ""
            # Write each dataframe to a different worksheet.

        if response_mem_win:
            sorted_data = sorted(response_mem_win['Datapoints'], key=lambda x: datetime.strptime(str(x['Timestamp']), '%Y-%m-%d  %H:%M:%S%z'))
            response_mem_win['Datapoints'] = sorted_data
            json_data_mem_win = json.dumps(response_mem_win["Datapoints"], default=datetime_handler)
            df2 = pd.DataFrame(eval(json_data_mem_win))
            df2.fillna('', inplace=True)
           
            # Write each dataframe to a different worksheet.
        
        
        print (df2.columns)        
        #return False
        df = pd.concat([df1,df2], axis=1, ignore_index=True)
        df=df.rename(columns = {0:'Timestamp', 1:'Average', 2:'Minimum',3:'Maximum', 4:'Unit', 5:'', 6:'Time', 7:'Avg', 8:'Min', 9:'Max', 10:'mem_unit'})
        df.columns = pd.MultiIndex.from_tuples(zip(['CPU-Utilization', '', '', '', '', 'MEMORY-Utilization', '', '', '', '', '', ''], df.columns))
        # df=df.rename(columns = { 0:'Maximum', 1:'Minimum',2:'Timestamp', 3:'Unit', 4:'', 5:'Max', 6:'Min', 7:'Time', 8:'mem_unit'})
        # df.columns = pd.MultiIndex.from_tuples(zip(['CPU-Utilization', '', '', '', 'MEMORY-Utilization', '', '', '', '', '', ''], df.columns))  
        df.index = df.index + 1  ## removing zero from index
        df.to_excel(writer, sheet_name=name)

    writer.save()
    writer.close

if __name__ == "__main__":
    d = get_all_instances()
    get_metrices(d)
# 10.235.201.13 typesetting3
# 10.235.201.139 typesetting4
# 10.235.201.130 typesetting5
# 10.235.200.5 spice 2
# 10.235.200.188 spice 6
# 10.235.200.217 spice 7
# 10.235.200.18  spice 8
# 10.235.200.34 spice 9
# 10.235.200.163 spice 13