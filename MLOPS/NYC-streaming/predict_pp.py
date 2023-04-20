import pickle
from flask import Flask, request,  jsonify
import mlflow
from mlflow.tracking import MlflowClient

#mlflow.set_tracking_uri("http://127.0.0.1:5000")
#mlflow.set_experiment("green-taxi-exp")
#get model from model registry

RUN_ID = 'def558fd38f44d8e9c4fc632668d3a47'


#no dv
#logged_model = F'runs:/{RUN_ID}/model' #model-uri
logged_model = f's3://mlflow-nyc-taxi-reg-exp/4/{RUN_ID}/artifacts/model'  #model-uri-s3

model = mlflow.pyfunc.load_model(logged_model)

def prepare_features(ride):
    features= {}
    features['PU_DO'] = '%s_%s' % (ride["PULocationID"],ride["DOLocationID"])
    features['trip_distance'] = ride["trip_distance"]
    return features

def predict(features):
    preds = model.predict(features)
    return float(preds[0])

#flask app
app = Flask('duration-prediction')


##flask wrapper
@app.route('/predict',methods=['POST'])
def predict_endpoint():
    ride = request.get_json()
    features = prepare_features(ride)
    pred = predict(features)
    result = {
        'duration': pred,
        'model_version':RUN_ID
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=9696)



    """
    {
        "ride" : {"PULocationID" : 130,
                  "DOLocationID" : 205,
                  "trip_distance" :3.66},
        "ride_id" : 123

    }
    """
    