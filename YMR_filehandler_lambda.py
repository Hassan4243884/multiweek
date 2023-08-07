import json
import boto3

s3 = boto3.client(
    "s3",
    region_name="us-east-1",
)

dynamoDB_handler = boto3.client(
    "dynamodb",
    region_name="us-east-1",
)


def lambda_handler(event, context):
    filename = event["queryStringParameters"]["file"]

    data = dynamoDB_handler.get_item(
        TableName="ymrdata", Key={"filename": {"S": filename}}
    )
    limit = int(data["Item"]["limit"]["N"])
    downloads = int(data["Item"]["downloads"]["N"])
    url = data["Item"]["url"]["S"]
    downloads += 1
    if downloads <= limit:
        dynamoDB_handler.update_item(
            TableName="ymrdata",
            Key={"filename": {"S": filename}},
            UpdateExpression=f"SET downloads = :downloads",
            ExpressionAttributeValues={":downloads": {"N": f"{downloads}"}},
        )
        return {
            "statusCode": 302,
            "headers": {"Location": url},
            "body": json.dumps(dict()),
        }

    else:
        try:
            s3.delete_object(
                Bucket="ymrmedia",
                Key=filename,
            )
        except:
            pass

        return {
            "statusCode": 404,
            "body": json.dumps({"details": "File has been deleted."}),
        }
