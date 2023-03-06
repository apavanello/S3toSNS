import boto3
import json


def lambda_handler(event, context):
    # Set up S3 client
    s3 = boto3.client('s3')

    # Set up SNS client
    sns = boto3.client('sns')

    # Get S3 bucket name and file key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    # Read the JSON file from S3
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    content = response['Body'].read().decode('utf-8')

    # Parse the JSON content
    data = json.loads(content)

    # Check if the data is a list
    if isinstance(data, list):
        # If the data is a list, publish each record to the SNS topic
        for record in data:
            sns.publish(
                TopicArn='YOUR_SNS_TOPIC_ARN',
                Message=json.dumps(record)
            )
    else:
        # If the data is not a list, publish the entire record to the SNS topic
        sns.publish(
            TopicArn='YOUR_SNS_TOPIC_ARN',
            Message=content
        )