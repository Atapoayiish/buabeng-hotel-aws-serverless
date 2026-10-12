# ReadLambda - GET /clients - For admin.html dashboard
import json, boto3, os

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        table = dynamodb.Table(os.environ['TABLE_NAME'])
        items = table.scan().get('Items', [])
        items.sort(key=lambda x: x.get('createdAt',''), reverse=True)
        return {'statusCode':200,'headers':{'Access-Control-Allow-Origin':'*'},'body':json.dumps(items)}
    except Exception as e:
        print(e)
        return {'statusCode':500,'headers':{'Access-Control-Allow-Origin':'*'},'body':json.dumps({"error":"Failed to fetch"})}