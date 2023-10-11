# Stock Prophet

Predicting stock prices using neural prophet. 
## Usage
make local prediction
```
conda activate stocker-neuralprophet
python3 app/model.py --ticker MSFT --days 7
```

## local: conda env    
```
conda create --name stocker-neuralprophet python=3.10
conda activate stocker-neuralprophet
pip install -r requirements.txt
```