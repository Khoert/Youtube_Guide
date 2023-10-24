# Youtube_Guide
This app creates summaries of Youtube videos by the topic of your choice, given a transcript is available on Youtube. 

The web app is based on the Streamlit framework, that employs 2 additional APIs: the Youtube and the [Anyscale](https://www.anyscale.com/) API. 
The former searches for the Youtube videos and the latter to provides high quality summaries from a Llama-2 70 B model. 

Finally, to query Youtube videos you need to have a Youtube API key. For instructions see https://developers.google.com/youtube/v3/getting-started. This API key must be added to the script YT_guide_v1.1.py in line 28. 
On the "YT guide" page you can enter your search term, for which Youtube videos should be summarized.





Screenshot:
![image](https://github.com/Khoert/Youtube_Guide/assets/140905959/065026f9-c71a-4d29-842d-685134225652)

The summary itself is available in the page "Read_out", where you can also create an audio if you wish.



Screenshot:
![image](https://github.com/Khoert/Youtube_Guide/assets/140905959/5298fd0e-62fe-433f-869f-bfebc3345b3a)


## Run locally

### Start

```shell
python -m pip install -r requirements.txt
python -m streamlit run path/to/YT_guide_v1.1.py
```
