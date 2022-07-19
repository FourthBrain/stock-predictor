# Stock Prophet

A demo for stock prophet deployment and hosting with FastAPI and AWS EC2

## Usage
```
curl \
    --header "Content-Type: application/json" \
    --request POST \
    --data '{"ticker":"MSFT", "days":7}' \
    http://35.90.247.255:8000/predict
```

You can access the interactive app [here](http://35.90.247.255:8000/docs#/default/get_prediction_predict_post)
