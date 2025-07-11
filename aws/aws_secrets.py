import boto3
import json
from botocore.exceptions import ClientError

def get_secret(secret_name="team9_indy9_login", region_name="us-east-2"):
    client = boto3.client("secretsmanager", region_name=region_name)
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response["SecretString"])
    except ClientError as e:
        raise Exception(f"Failed to fetch secret: {e}")
