import json
import base64
import boto3
import os
import mlflow


RUN_ID = 'def558fd38f44d8e9c4fc632668d3a47'
logged_model = f's3://mlflow-nyc-taxi-reg-exp/4/{RUN_ID}/artifacts/model'  #model-uri-s3
model = mlflow.pyfunc.load_model(logged_model)
#'s3://mlflow-nyc-taxi-reg-exp/4/def558fd38f44d8e9c4fc632668d3a47/artifacts/model'


TEST_RUN = os.getenv('TEST_RUN', 'False')  == 'False'
kinesis_client = boto3.client('kinesis')
PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME','ride_prediction')


def prepare_features(ride):
    features= {}
    features['PU_DO'] = '%s_%s' % (ride["PULocationID"],ride["DOLocationID"])
    features['trip_distance'] = ride["trip_distance"]
    return features


def predict(features):
    pred= model.predict(features) 
    return float(pred[0])

    

def lambda_handler(event, context):
    #print(json.dumps(event))
    prediction_events = []
    
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        ride_event = json.loads(decoded_data)
	    
        #print(ride_event)
        ride = ride_event['ride']
        ride_id = ride_event['ride_id']
        features = prepare_features(ride)
        prediction = predict(features)
            
        prediction_event = {
        'model' : 'ride_duration_prediction_model',
        'version': 123,
        'prediction': {
            'ride_duration': prediction,
            'ride_id': ride_id
            }
        }
        
        prediction_events.append(prediction_event)

        if not TEST_RUN:
            kinesis_client.put_record(
                StreamName=PREDICTIONS_STREAM_NAME,
                Data = json.dumps(prediction_event),
                PartitionKey = str(ride_id)
                )
    print(prediction_events)
        
    return {
        'predictions': prediction_events
    }   