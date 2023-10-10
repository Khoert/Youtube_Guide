# Youtube_Guide
This app creates summaries of Youtube videos by the topic of your choice, \bold{given} a transcript is available on Youtube. The web app is based on the Streamlit framework, while the summary is generated with the BART LLM model provided on Huggingface, see the https://huggingface.co/facebook/bart-large-cnn. Note, during the first run, the BART model is downloaded locally, this may take some time. 


![image](https://github.com/Khoert/Youtube_Guide/assets/140905959/c2862abd-fad9-48f6-97f5-9e274c81c55f)


Finally, to query Youtube videos you need to have a Youtube API key. For instructions see https://developers.google.com/youtube/v3/getting-started. This API key must be added to the script YT_guide_v1.1.py in line 28. 

On the "YT guide" page you can enter your search term, for which Youtube videos should be summarized.   

![image](https://github.com/Khoert/Youtube_Guide/assets/140905959/82d2df27-4fd4-4ed3-9267-146fbcbe1987)

Given a transcript exists a summary is generated. 

![image](https://github.com/Khoert/Youtube_Guide/assets/140905959/065026f9-c71a-4d29-842d-685134225652)

The summary itself is available in the page "Read_out", where you can also create an audio if you wish.

![image](https://github.com/Khoert/Youtube_Guide/assets/140905959/5298fd0e-62fe-433f-869f-bfebc3345b3a)


## Run locally

### Start

```shell
python -m pip install -r requirements.txt
python -m streamlit run path/to/YT_guide_v1.1.py
```
