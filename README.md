# Youtube_Guide
This app creates summaries of Youtube videos by the topic of your choice, given a transcript is available on Youtube. 

The web app is based on the Streamlit framework, that employs 2 additional APIs: 
- the Youtube API
- and the [Anyscale](https://www.anyscale.com/) API. 

The latter to provides high quality summaries from a Llama-2 70 B model at a low cost of 1$ per 1 Mio tokens.  

To use the Youtube Guide you need to sign on for both API keys. 
For the Youtube API key instructions see https://developers.google.com/youtube/v3/getting-started. This API key must be added to the script YT_guide_v1.1.py in line 28. 
The Anyscale API instructions are available on https://app.endpoints.anyscale.com/

## Usage:
On the "YT guide" page you can enter your search term, for which Youtube videos will be summarized.  
On the "Read out" page you can retrieve all summaries you generated before. Addtionally you can generate an audio instead of reading the summary. 


### Installation

### 

```shell
python -m pip install -r requirements.txt
python -m streamlit run path/to/YT_guide_v1.1.py
```
