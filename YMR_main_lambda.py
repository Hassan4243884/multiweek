import boto3
from botocore.exceptions import ClientError
import json


def lambda_handler(event, context):
    sender = "YMR <ywuvjo@exelica.com>"

    emails = event["emails"]
    download_url = f"https://v9mrch26s9.execute-api.us-east-1.amazonaws.com/S3/download_file?file={event['filename']}"
    count = len(event["emails"])

    html_message = f"""
    <html>
    <head></head>
    <body>
    <h1>
        Download the uploaded file <a href="{download_url}" >{event['filename']}</a>
    </h1>
    </body>
    </html>

    """

    ses_client = boto3.client("ses", region_name="us-east-1")
    try:
        if count > 0:
            ses_client.send_email(
                Destination={
                    "ToAddresses": emails,
                },
                Message={
                    "Body": {
                        "Html": {
                            "Charset": "UTF-8",
                            "Data": html_message,
                        },
                        "Text": {
                            "Charset": "UTF-8",
                            "Data": download_url,
                        },
                    },
                    "Subject": {
                        "Charset": "UTF-8",
                        "Data": "Download the Upload File",
                    },
                },
                Source=sender,
            )

    except ClientError as e:
        body = e.response["Error"]["Message"]
    else:
        body = ("Worked Great",)
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,DELETE,POST,PATCH,OPTIONS",
            "Access-Control-Allow-Headers": "access-control-allow-credentials,access-control-allow-headers,access-control-allow-methods,Access-Control-Allow-Origin,authorization,content-type",
            "Content-Type": "application/json",
        },
        "body": json.dumps(body),
    }
