import json
import boto3
from time import gmtime, strftime
from decimal import Decimal
import decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('end2end_web_db')

def lambda_handler(event, context):
    print(event) # 加入此行
    http_method = event.get('httpMethod') # 使用 event.get() 安全存取

    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': 'https://staging.d1znnw2eq380dx.amplifyapp.com',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps('CORS preflight successful!')
        }
        
    now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    num1 = None
    num2 = None
    operator = None
    result = None

    try:
        body = json.loads(event['body'])
        num1 = Decimal(str(body['num1']))
        num2 = Decimal(str(body['num2']))
        operator = body['operator']

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Access-Control-Allow-Origin': 'https://staging.d1znnw2eq380dx.amplifyapp.com',
                        'Access-Control-Allow-Methods': 'POST, OPTIONS',
                        'Access-Control-Allow-Headers': 'Content-Type',
                    },
                    'body': json.dumps({'error': '除數不能為零'})
                }
            result = num1 / num2
        else:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': 'https://staging.d1znnw2eq380dx.amplifyapp.com',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type',
                },
                'body': json.dumps({'error': '無效的運算符'})
            }

        table.put_item(
            Item={
                'id': now,
                'num1': result_to_decimal(num1),
                'num2': result_to_decimal(num2),
                'operator': operator,
                'result': result_to_decimal(result)
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': 'https://staging.d1znnw2eq380dx.amplifyapp.com',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({'result': str(result)})
        }

    except (json.JSONDecodeError, KeyError) as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': 'https://staging.d1znnw2eq380dx.amplifyapp.com',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({'error': f'無效的 JSON 請求體：{str(e)}'})
        }
    except (ValueError, TypeError, decimal.InvalidOperation) as e:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': 'https://staging.d1znnw2eq380dx.amplifyapp.com',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({'error': f'無效的請求：{str(e)}'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': 'https://staging.d1znnw2eq380dx.amplifyapp.com',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({'error': f'伺服器錯誤：{str(e)}'})
        }

def result_to_decimal(result):
    return Decimal(str(result))