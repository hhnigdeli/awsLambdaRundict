import json
import boto3
from rundict import kml_to_df

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('rundictRoutes')

def route_reader(event, context):
    
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    user = event["Records"][0]["s3"]["object"]["eTag"]
    
    
    obj = s3.get_object(Bucket=bucket, Key=key)
    
    route = obj["Body"].read()

    routeJson = kml_to_df(route)
    
    table.put_item(
    Item={
        'name': key,
        'user': user,
        'route':routeJson
        
    }
    )
    
    print("Data Saven on DynamoDB for: {}".format(user))