Ride trip duration prediction steaming app using AWS lambda and kinesis
-----------------------------------------------------------------------

App details: Trip duration prediction 
Data: NYC Green trip data 2022 Jan, Feb
Features used for training: PickUp location, DropOff Location, trip_distance,PU_DO (DictVectorizer used to map features to vectors)
Model details : s3://mlflow-nyc-taxi-reg-exp/4/def558fd38f44d8e9c4fc632668d3a47/artifacts/model (RandomForestRegressor Implemented in python (params:max_depth-20, min_samples_leaf-10,n_estimators-100,random_state-0,rmse:6.101)), mlflow was used for experiment tracking.

About the Project:
The Lambda function ride_duration_prediction prepares features from a json input event, fetches the model from s3, and predicts the trip-duration using the model.  The lambda function is containerised using Docker and the image is published on ECR registry. Event data is put on to the ride_events kinesis data stream as json and the predictions are fetched by the ride_prediction kinesis data stream using get_record method in aws cli.


Steps to create the streaming app:
1) create IAM role and set permissions: 
lambda-kinesis-role (role-name), select trusted entity-lambda, and awslambdakinesisexecutionrole

2) Starting with lambda,to ensure output on an event test  
create a test lambda function with lambda_handler, and test it  with readily available event configuration:
ride-duration-prediction-function, py 3.9,lambda-kinesis-role

function code-

import json
#event is a dictionary,if lambda is connected to an endpoint then
 event can be any requests comng to this endpoint

def lambda_handler(event, context):
    # TODO implement
    print (json.dumps(event))
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
 3) Improve lambda function by adding prepare_features and sample predict_features functions and configure test event with a basic ride event(json)

function code:

function-import json

def prepare_features(ride):
    features= {}
    features['PU_DO'] = '%s_%s' % (ride["PULocationID"],ride["DOLocationID"])
    features['trip_distance'] = ride["trip_distance"]
    return features


def predict(features):
    return 10.0
    

def lambda_handler(event, context):
    ride = event['ride']
    ride_id = event['ride_id']
    features = prepare_features(ride)
    predictions = predict(features)
    
    return {
        'ride_duration': predictions,
        'ride_id': ride_id
    }
    
    
    
    event test data:

{
  "ride": {
    "PULocationID": 130,
    "DOLocationID": 205,
    "trip_distance": 3.66
  },
  "ride_id": 123
}

4) check how kinesis stream put event format is by put_record-ing the basic test event from aws cli and reading the cloudwatch logs of aws lambda function 

function code (with edits):
import json

def prepare_features(ride):
    features= {}
    features['PU_DO'] = '%s_%s' % (ride["PULocationID"],ride["DOLocationID"])
    features['trip_distance'] = ride["trip_distance"]
    return features


def predict(features):
    return 10.0
    

def lambda_handler(event, context):
    #ride = event['ride']
    #ride_id = event['ride_id']
    #features = prepare_features(ride)
    #predictions = predict(features)
    
    print(json.dumps(event))
    predictions = 10.0 
    
    return {
        'ride_duration': predictions,
        'ride_id': ride_id
    }

Steps to do:
Create kinesis stream ride_events (-data stream,-prov mode, 1 shard)
At lambda, add trigger -kinesis stream - ride_events
configure aws cli for iam user with access keys and secret key-output format=text
create test event and send through terminal(PutRecord returns the shard ID of where the data record was placed and the sequence number that was assigned to the data record.
Writes a single data record into an Amazon Kinesis data stream)

format:
aws kinesis put-record \
	--stream-name ride_events \
	--partition-key 1 \
	--data "Hi test 1"
	--cli-binary-format raw-in-base64-out
	
In aws terminal, obtain the shard details 
Lambda will consume this from streams and it will be reflected in the logs.
Check lambda monitor- logs in cloudwatch for event structure

Obtained event structure:

{
    "Records": [
         {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49639854210870046278837730611666112709822541697829044226",
                "data": "SGkgdGVzdCAx",
                "approximateArrivalTimestamp": 1681551089.843
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49639854210870046278837730611666112709822541697829044226",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::938316853267:role/lambda-kinesis-role",
            "awsRegion": "us-east-1",
            "eventSourceARN": "arn:aws:kinesis:us-east-1:938316853267:stream/ride_events"
        }
    
    ]
}


To decode the event data using base64 modify lambda function :

function code:

import base64

for record in event['Records']:
	encoded_data = record['kinesis']['data']
	decoded_data = base64.b64decode(encoded_data).decode('utf-8')
	print(decoded_data)



Now, edit the test, create a new test and paste the event with encoded text to check if it gives the decoded output


5)Deploy and test sending ride record

At aws cli:

aws kinesis put-record \
	--stream-name ride_events \
	--partition-key 1 \
	--cli-binary-format raw-in-base64-out \
	--data '{
  "ride": {
    "PULocationID": 130,
    "DOLocationID": 205,
    "trip_distance": 3.66
  },
  "ride_id": 123
}
'


Event config from AWS lambda log: 


{
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

Now decode the ride data with lambda function

6) Creating the kinesis stream to consume the prediction outputs

Create the stream - ride_prediction

Modified lambda function:

import boto3
kinesis_client = boto3.client('kinesis')
prediction_events=[]
PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME','ride_prediction')

lambda_handler():
.
.
.
.
kinesis_client.put_record(
	StreamName=PREDICTIONS_STREAM_NAME,
	Data : json.dumps(prediction_event),
	PartitionKey: str(ride_id)
)


Attach a policy to lambda-kinesis role to provide putRecord permission to lambda
(iam-permission-attach policy-create policy-kinesis service-action write-putrecord/s-resource stream arn-....ride_predictions)


To get_records from ride_prediction stream, at AWS cli:

export KINESIS_STREAM_OUTPUT='ride_prediction'
export SHARD='shardId-000000000000'
export SHARD_ITERATOR=$(aws kinesis \
	get-shard-iterator \
	--shard-id ${SHARD} \
	--shard-iterator-type TRIM_HORIZON \
	--stream-name ${KINESIS_STREAM_OUTPUT} \
	--query 'ShardIterator'
	)

echo $SHARD_ITERATOR

export RESULT=$(aws kinesis get-records --shard-iterator $SHARD_ITERATOR --output json)

echo $RESULT

(apt-get install jq   # to pick json objects )

echo ${RESULT} | jq -r '.Records[0].Data' | base64 --decode |jq


7) Adding model to lambda function

Edit the lambda function locally, adding model details

code:

import mlflow
.
.
.
.
model = ...(logged_model)
TEST_RUN = os.getenv('TEST_RUN', 'False')  == 'True'

pred= model.predict(features) 
return float(pred[0])


if not TEST_RUN:
	kinesis.client_put....

create test.py

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



in the terminal:
cd to folder containing lambda_function
pipenv shell
python3 test_lambda_function.py



'''
export PREDICTIONS_STREAM_NAME='ride_prediction'
export RUN_ID='def558fd38f44d8e9c4fc632668d3a47' 
export TEST_RUN="True"

python3 test_.py


'''

7) Packaging to a docker container

pipenv install boto3 mlflow scikit-learn --python=3.9

Create Dockerfile- copy image tag from  search  'aws ecr registry'  -lambda py-image tags-3.9 copy image)

Dockerfile:

FROM public.ecr.aws/lambda/python:3.9

RUN pip install -U pip
RUN pip install pipenv

RUN pip install -U pip
RUN pip install pipenv

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

copy ["lambda_function", "./"]
CMD ["lambda_function.lambda_handler"]


cd to folder containing lambda_function, Dockerfile, Pipfile,..

build the docker:
docker build -t stream-model-duration:v1 .

run docker:
docker run -it --rm \
	-p 8080:8080 \
	-e PREDICTIONS_STREAM_NAME="ride_prediction" \
	-e RUN_ID='def558fd38f44d8e9c4fc632668d3a47' \
	-e TEST_RUN="True" \
	-e AWS_ACCESS_KEY_ID="**********************" \
	-e AWS_SECRET_ACCESS_KEY="**************************" \
	-e AWS_DEFAULT_REGION="us-east-1" \
	stream-model-duration:v1

create requests (test_docker.py) and test to check if docker image is working

test_docker:

import requests
.
.
.
url=  'http://localhost:8080/2015-03-31/functions/function/invocations'
response = request.post(url, json=event)
print(response.json())
#http post method


cd to folder containing lambda_function, Dockerfile, Pipfile,..
python3 test_docker

docker and pipenv commands:
docker ps
docker kill cid
docker image rm stream-model-duration:v1 

pipenv --rm
rm Pipfile.lock
pipenv install

reference: https://aripalo.com/blog/2020/aws-lambda-container-image-support/


8) Publish to ecr (docker registry)
aws cli:
aws ecr create-repository --repository-name duration-pred-model
(get repository uri from command output)
<user>.dkr.ecr.<region>.amazonaws.com/duration-pred-model

Now, authenticate docker with ecr:
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <user>.dkr.ecr.<region>.amazonaws.com/

export REMOTE_URI="<user>.dkr.ecr.<region>.amazonaws.com/duration-pred-model"
export REMOTE_TAG='v1'
export REMOTE_IMAGE=${REMOTE_URI}:${REMOTE_TAG}
export LOCAL_IMAGE="stream-model-duration:v1"

docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
docker push ${REMOTE_IMAGE}

echo $REMOTE_IMAGE
<user>.dkr.ecr.<region>.amazonaws.com/duration-pred-model:v1
Use this image to create the new aws lambda function

9) AWS lambda (new function) remove the older one

create new function using container image-ride_duration_prediction-give container image uri-provide lambda kinesis role 

configure function-add environment variables-prediction_stream_name,run_id

add trigger-kinesis-ride_events

In terminal send event
(aws kinesis put-record .......)

And view logs in lambda

Attach policy for reading s3 bucket to lambda-kinesis role
(iam role-add permission-attach policy-s3-read,list permissions-resources-bucket-give bucket name to be read from -object-b name, * for obj name)

test with event using test_docker.py

config lambda-edit basic settings-256/512mb memory-15s timeout

Now, the real part..

Send event record through ride_events stream
(aws kinesis put_record ....) and receive the predictions from ride_prediction stream online (aws kinesis get_record...)
