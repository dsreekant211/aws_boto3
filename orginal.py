import boto3
from datetime import datetime
import json
from bson import json_util
import pandas as pd
import numpy as np
import xlsxwriter

writer = pd.ExcelWriter('Metrics.xlsx', engine='xlsxwriter')

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
            StartTime=datetime(2019,11,10),
            EndTime=datetime(2019,11,12),
            Period=3600 ,
            Statistics=[
                'Average','Minimum','Maximum',
            ],
            Unit='Percent'            
        )

        response_mem = client.get_metric_statistics(
            Namespace='CWAgent',
            MetricName='mem_used_percent',
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
            ],
            StartTime=datetime(2019,11,10),
            EndTime=datetime(2019,11,12),
            Period=3600 ,
            Statistics=[
                'Average','Minimum','Maximum',
            ],
            Unit='Percent'
        )        
        
        if response:
            sorted_data = sorted(response['Datapoints'], key=lambda x: datetime.strptime(str(x['Timestamp']), '%Y-%m-%d  %H:%M:%S%z'))
            response['Datapoints'] = sorted_data
            json_data = json.dumps(response["Datapoints"], default=datetime_handler)
            df1 = pd.DataFrame(eval(json_data))
            df1.fillna('', inplace=True)
            df1["C"] = ""
            # Write each dataframe to a different worksheet.

        if response_mem:
            sorted_data = sorted(response_mem['Datapoints'], key=lambda x: datetime.strptime(str(x['Timestamp']), '%Y-%m-%d  %H:%M:%S%z'))
            response_mem['Datapoints'] = sorted_data
            json_data_mem = json.dumps(response_mem["Datapoints"], default=datetime_handler)
            df2 = pd.DataFrame(eval(json_data_mem))
            df2.fillna('', inplace=True)
            # Write each dataframe to a different worksheet.
        
        #df = pd.concat([df1,df2])
        #df = pd.merge(left=df1,right=df2)
        print (df2.columns)        
        #return False
        df = pd.concat([df1,df2], axis=1, ignore_index=True)
        df=df.rename(columns = {0:'Average', 1:'Maximum', 2:'Minimum',3:'Timestamp', 4:'Unit', 5:'', 6:'Avg', 7:'Max', 8:'Min', 9:'Time', 10:'mem_unit'})
        df.columns = pd.MultiIndex.from_tuples(zip(['CPU-Utilization', '', '', '', '', 'MEMORY-Utilization', '', '', '', '', '', ''], df.columns)) 
        #df = pd.merge(left=df1,right=df2, how="outer")
        df.to_excel(writer, sheet_name=name)

    writer.save()
    writer.close

if __name__ == "__main__":
    d = get_all_instances()
    print("response", d)
    get_metrices(d)