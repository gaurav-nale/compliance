import boto3
import pandas as pd
import io
import pymysql
from sqlalchemy import create_engine
import json
import urllib.parse

bedrock_client = boto3.client(
    service_name = 'secretsmanager',
    region_name = "us-east-2",
    aws_access_key_id='ASIA3FLD26ANMCIZGU2A',
    aws_secret_access_key='1IRmGIOJ8nDOEqmKr7JVOGKPA/kvOTFY0qh9nDww',
    aws_session_token = 'IQoJb3JpZ2luX2VjEF4aCXVzLWVhc3QtMSJHMEUCIQDIx839n5dI/BYcw9YcqWeBStCvmHDjf3hx6wIzBC6u4gIgPd8n18VQkVRgTArq+dEpcE35b5WxdZt8SCqN9hk44OAq/AIIp///////////ARAAGgw3NjczOTc5MTY2OTgiDLa8MPZE9pUWr1ZD/irQAhcQfCJ4/ejdZktZ7iaymvaSTMV91rO2ZqKNTh9wt5v0w7P2TbLKOQKUPiwLgbM9+jTwqSLYsjcvlxUNNy+34L0oguROr8DSCHC/z2zuc7cdusgeuoZTg/WO4pc1Bgeg8ZnQS7zGfZeKuUj+paovTBf8q31uUIokZCjqbT0cHGBriAf+pVAYmIxjYb+7hx7H9nxHc3FsE/scAP5n/t8CuksESxF94Hsj2vRQ5cLiR+vhSggfNF1W7zyYrXgEM1a5zGy5XErhUJwg4Xbv+tXeCmmDb2QQGYSrFTi7dwnDbmAYVyrDKLAwS5lUXylbGBTLWcuW+5nkq7zL3pVkcnmA/DTkk6+I7kE7YGVRQ6ldKggSDIiqnLk5CJaPcYWgxIdA9EkBQHLBz1q12oIrwnZOQqYddGKQQLJE+q1Bw/ZY/6GcloHieAJ8Mo2YSKmPpH8zZjC5g8G+BjqnAUONYCbKj4M8NcS4DrzDJjz7xE36xrOvz+BRa6rt4XuMt3ZUl93xSF9ESr+FSFSGGdeDuB2DsY3CRiXdSTtYgEfJfX5AnjM7A7AyjtdnxaIG6w1B1K7kI/+1T9j0BJi7HoHVmB8znkkYjHPnwizcW3NBlgPVJxVQaCf0hv0YAY5UqTEfBV1n6Cs3Yp0QGd8JvZ95ZrUTtcseuIkxZ4VNrJ9br4IJB3vj'
)

AURORA_SECRET_ARN = "arn:aws:secretsmanager:us-east-2:767397916698:secret:BedrockUserSecret-lcavPl3SIQF6-RrAdZN"

def get_db_credentials():
    response = bedrock_client.get_secret_value(SecretId=AURORA_SECRET_ARN)
    secret_dict = json.loads(response["SecretString"])
    return secret_dict

def get_db_connection():
    creds = get_db_credentials()
    db_user = urllib.parse.quote_plus(creds["username"])
    db_password = urllib.parse.quote_plus(creds["password"])
    db_host = "knowledgebasequickcreateaurora-007-auroradbcluster-nehjn66dsqz7.cluster-ctc0s4my8k73.us-east-2.rds.amazonaws.com"  # Use actual endpoint
    db_name = "Bedrock_Knowledge_Base_Cluster"
    return create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}?connect_timeout=1000")

def fetch_latest_data():
    try:
        engine = get_db_connection()
        with engine.connect() as conn:
            return pd.read_sql("SELECT id, text, vector FROM bedrock_integration.bedrock_knowledge_base", conn)
    except Exception as e:
        print("Error: ",str(e))

def update_aurora():
    existing_data = fetch_latest_data()
    print(existing_data)

update_aurora()