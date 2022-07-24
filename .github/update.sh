for ticker in MSFT AAPL GOOG FB AMZN INTL CVX MRK
do
    echo "Updating $ticker"
    python src/model.py --ticker $ticker --days 7
done