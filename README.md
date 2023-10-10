# Youtube_Guide
This app creates summaries of Youtube videos by the topic of your choice, given a transcript is available on Youtube. The web app is based on the Streamlit framework, while the summary is generated with the BART LLM model provided on Huggingface, see the https://huggingface.co/facebook/bart-large-cnn. Note, during the first run, the BART model is downloaded locally, this may take some time. 


![image](https://github.com/Khoert/Youtube_Guide/assets/140905959/c2862abd-fad9-48f6-97f5-9e274c81c55f)


Finally, to query Youtube videos you need to have a Youtube API key. For instructions see https://developers.google.com/youtube/v3/getting-started. This API key must be added to the script YT_guide_v1.1.py in line 28. 

## Run locally

### Start

```shell
python -m pip install -r requirements.txt
python -m streamlit run path/to/YT_guide_v1.1.py
```
