import json
import boto3
from rundict import kml_to_df, add_distance

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('rundictRoutes')
table1 = dynamodb.Table('rundictDistances')

def route_reader(event, context):
    
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    user = event["Records"][0]["s3"]["object"]["eTag"]
    
    
    obj = s3.get_object(Bucket=bucket, Key=key)
    
    route = obj["Body"].read()

    routeJson = kml_to_df(route)
    distances = add_distance(routeJson)
    
    table.put_item(
    Item={
        'name': key[:-4],
        'user': user,
        'route':routeJson
        
    }
    )

    table1.put_item(
    Item={
        'name': key[:-4],
        'user': user,
        'dist':distances
        
    }
    )
    
    print("Data Saven on DynamoDB for: {}".format(user))