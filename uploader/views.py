from django.shortcuts import render, redirect
from django.http.response import HttpResponse
import boto3
import json


REGION = "us-east-1"
Table_Name = "ymrdata"

FunctionName = "lambdafunction"


s3 = boto3.client(
    "s3",
    region_name="us-east-1",
)

dynamoDB_handler = boto3.client(
    "dynamodb",
    region_name="us-east-1",
)


def upload_file(request):
    if request.method == "POST":
        request_data = request.POST
        emails = [email for email in request_data.getlist("email") if email]
        file = request.FILES.get("file")

        filename = file.name
        s3.upload_fileobj(file, "ymrmedia", filename)
        download_url = f"https://ymrmedia.s3.amazonaws.com/{filename}"
        limit = str(len(emails))

        dynamoDB_handler.put_item(
            TableName="ymr-table",
            Item={
                "filename": {"S": filename},
                "downloads": {"N": "0"},
                "url": {"S": download_url},
                "limit": {"N": str(limit)},
            },
        )

        lambda_function = boto3.client("lambda", region_name="us-east-1")

        lambda_function.invoke(
            FunctionName="lambdafunction",
            InvocationType="RequestResponse",
            Payload=json.dumps(
                {"filename": filename, "emails": emails, "url": download_url}
            ),
        )

        return render(request, "result.html")


def index(request):
    return render(request, "base.html")
