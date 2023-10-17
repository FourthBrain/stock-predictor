# Stock Predictor

Predicting stock prices using neural prophet. 
## Usage
make local prediction
```
conda activate stock-predictor
python3 app/model.py --ticker MSFT --days 7
```

## local: conda env    
```
conda create --name stock-predictor python=3.10 -y
conda activate stock-predictor
pip install -r requirements.txt
```