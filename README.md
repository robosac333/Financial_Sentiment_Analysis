# Financial_Sentiment_Analysis
A financial statement analysis using Natural Language Understanding.

## Setup

### Create a Conda environment

```sh
conda create -n chatbot python=3.10.15
```
### Get all the dependencies
```sh
pip -r install requirements.txt
```
NOTE : 
1. I have configured the pipeline to utilize CPU-based inference to ensure seamless execution, mitigating potential compatibility issues between the CUDA version and Torch. This approach guarantees that the invigilator can run the container without any disruptions.

2. The FMP and Finnhub API keys to fetch latest news and summary were paid and needed subscription. As a result I used only the Alpha Vantage API to get the required information.

3. Normally, the .env file would be included in the .gitignore to ensure the credentials are stored securely. However, in this case, it has been intentionally included to simplify the setup process for the invigilator, as the token used is freely available and does not pose a security risk.

### Activate the app
```sh
python app.py
```
### Query a Ticker
After the app gets activated you may connect to the app by querying the required ticker at the following address.Replace the ticker attribute with the company ticker you want to enquire.
```sh
http://localhost:5000/api/v1/sentiment?ticker=AAPL
```