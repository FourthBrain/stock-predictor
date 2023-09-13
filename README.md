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
1. conda env    

    ```
    conda create --name stocker-neuralprophet python=3.10
    conda activate stocker-neuralprophet
    pip install -r requirements.txt
    ```
1. uvicorn 
    ```
    cd app
    uvicorn  main:app --workers 1 --host 0.0.0.0 --port 8000
    ```
    if not working: fnd the path of uvicorn and add it to the path
    ```
    conda env list 

    /Users/flora/miniforge3/envs/stocker-neuralprophet/bin/uvicorn main:app --workers 1 --host 0.0.0.0 --port 8000

    curl localhost:8000/ping
    
    curl \
    --header "Content-Type: application/json" \
    --request POST \
    --data '{"ticker":"MSFT", "days":7}' \
    http://localhost:8000/predict
    ```
2. docker. 
docker run -d --rm --name mycontainer -p 8000:8000 stock-prophet
```
docker build -t stock-neuralprophet .
docker run -p 8000:8000 stock-neuralprophet  # one can see the log
docker run -d --rm --name mycontainer -p 8000:8000 stock-neuralprophet   # behind the scene


curl localhost:8000/ping

curl \
--header "Content-Type: application/json" \
--request POST \
--data '{"ticker":"MSFT", "days":7}' \
http://localhost:8000/predict
```


3 streamlit ( local )
```
python3 streamlit run stock_ui.py
```
#TODO: is this the best structure? 