import os
import boto3

# from dotenv import load_dotenv
# load_dotenv()

def get_dynamodb_conn():
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.environ.get('FAST_API_AWS_REGION'),
        aws_access_key_id=os.environ.get('FAST_API_AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('FAST_API_AWS_SECRET_ACCESS_KEY')
    )

    return dynamodb