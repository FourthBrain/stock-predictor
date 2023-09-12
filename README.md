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


## local
1. uvicorn `/Users/flora/miniforge3/envs/stock-arima/bin/uvicorn  main:app --reload --workers 1 --host 0.0.0.0 --port 8000`

2. docker. 
```
docker build -t stock-nueralprophet .
docker run -p 8000:8000 stock-nueralprophet  
curl localhost:8000/ping

curl \
--header "Content-Type: application/json" \
--request POST \
--data '{"ticker":"MSFT", "days":7}' \
http://localhost:8000/predict
```