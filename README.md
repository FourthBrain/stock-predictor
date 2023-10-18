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
1.  conda env    
    ```
    conda create --name sp-fastapi python=3.10 -y
    conda activate sp-fastapi
    pip install -r requirements.txt
    ```

1. uvicorn 
    ```
    cd app
    uvicorn  main:app --reload --host 0.0.0.0 --port 8000
    ```
