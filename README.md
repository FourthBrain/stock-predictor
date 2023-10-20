# Stock Predictor

wrap the ML model into an API via fastapi 

## Usage

```
conda activate sp-fastapi

curl localhost:8000/ping
    
curl \
--header "Content-Type: application/json" \
--request POST \
--data '{"ticker":"MSFT", "days":7}' \
http://localhost:8000/predict
```



## local setup
```
docker build -t stock-predictor .
docker run -d --rm --name mycontainer -p 8000:8000 stock-predictor
```