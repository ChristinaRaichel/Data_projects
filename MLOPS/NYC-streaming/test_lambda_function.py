import lambda_function

event = {
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49639854210870046278837730620094743524175848591505489922",
                "data": "ewogICJyaWRlIjogewogICAgIlBVTG9jYXRpb25JRCI6IDEzMCwKICAgICJET0xvY2F0aW9uSUQiOiAyMDUsCiAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICB9LAogICJyaWRlX2lkIjogMTIzCn0K",
                "approximateArrivalTimestamp": 1681552724.5
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49639854210870046278837730620094743524175848591505489922",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::938316853267:role/lambda-kinesis-role",
            "awsRegion": "us-east-1",
            "eventSourceARN": "arn:aws:kinesis:us-east-1:938316853267:stream/ride_events"
        }
    ]
}

result = lambda_function.lambda_handler(event,None)
print(result)
