# SaveLambda - POST /clients - Saves booking from website
import json, boto3, os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    try:
        body = json.loads(event.get('body', '{}'))
        if not body.get('phone') or not body.get('name'):
            return {'statusCode':400,'headers':{'Access-Control-Allow-Origin':'*'},'body':json.dumps({"error":"Name and phone required"})}
        
        item = {
          'phone': body['phone'].strip(),
          'name': body['name'].strip(),
          'roomType': body.get('roomType','Standard'),
          'source': body.get('source','Website'),
          'createdAt': datetime.utcnow().isoformat()
        }
        table.put_item(Item=item)
        return {'statusCode':200,'headers':{'Access-Control-Allow-Origin':'*'},'body':json.dumps({"message":"Saved"})}
    except Exception as e:
        print(e)
        return {'statusCode':500,'headers':{'Access-Control-Allow-Origin':'*'},'body':json.dumps({"error":"Internal error"})}