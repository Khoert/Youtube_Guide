# Youtube_Guide
This app creates summaries of Youtube videos by the topic of your choice, given a transcript is available on Youtube. 

The web app is based on the Streamlit framework, that employs 2 additional APIs: 
- the Youtube API
- and the [Anyscale](https://www.anyscale.com/) API. 

The latter to provides high quality summaries from a Llama-2 70 B model at a low cost of 1$ per 1 Mio tokens.  

To use the Youtube Guide you need to sign on for both API keys. 
For the Youtube API key instructions see https://developers.google.com/youtube/v3/getting-started. 
The Anyscale API instructions are available on https://app.endpoints.anyscale.com/. 


This API key must be added to the script YT_guide_v2.py in line 38. 
This API key must be added to the script YT_guide_v2.py in line 28. 

## Usage:
On the "YT guide" page you can enter your search term, for which Youtube videos will be summarized.  
On the "Read out" page you can retrieve all summaries you generated before. Addtionally you can generate an audio instead of reading the summary. 


### Installation
1. Clone the repository 
   1.1. Open Powershell and go to the location of your choice e.g. C:\Users\xyz
   1.2. Clone the repository with the Powershell command "git clone https://github.com/Khoert/Youtube_Guide.git"
2. Installing   
   2.1. In Powershell change to the installed repository, where requirements.txt is located
   2.2. Install all packages required for the app with the command: "python -m pip install -r requirements.txt"
3. Add the API keys
   3.1. Outside of Powershell open the file YT_guide_v2.py of the installed repository
   3.2. Add the Anyscale API key in line 28 of  script YT_guide_v2.py
   3.3. Add the Youtube API key in line 38 of  script YT_guide_v2.py       
4. Running the app
   3.1. Go back to Powershell
   3.2. Change to the location in the installed repository, where YT_guide_v2.py is located
   3.2. Start the app in your web browser with the command "python -m streamlit run path/to/YT_guide_v2.py"
