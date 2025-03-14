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
NOTE : I have configured the pipeline to utilize CPU-based inference to ensure seamless execution, mitigating potential compatibility issues between the CUDA version and Torch. This approach guarantees that the invigilator can run the container without any disruptions.

Also, the FMP and Finnhub API keys to fetch latest news and summary were paid and needed subscription. As a result I used only the Alpha Vantage API to get the required information.