# Youtube_Guide
This app creates summaries of Youtube videos by the topic of your choice, given a transcript is available on Youtube. 

The web app is based on the Streamlit framework, that employs 2 additional APIs: 
- the Youtube API
- and the [Anyscale](https://www.anyscale.com/) API. 

The latter to provides high quality summaries from a Llama-2 70 B model at a low cost of 1$ per 1 Mio tokens.  

To use the Youtube Guide you need to sign on for both API keys. 
For the Youtube API key instructions see https://developers.google.com/youtube/v3/getting-started. 
The Anyscale API instructions are available at https://app.endpoints.anyscale.com/. 

## Usage

First, enter the Youtube and Anyscale API keys on the right side. 

<img width="800" alt="Screenshot 2023-12-02 at 19 29 11" src="https://github.com/Khoert/Youtube_Guide/assets/140905959/555cbb2f-17b8-40bc-b8fb-dccd05246bde">


On the "YT guide" page you can enter your search term, for which Youtube videos will be summarized.  
On the "Read out" page you can retrieve all summaries you generated before. Additionally, you can generate an audio instead of reading the summary. 


https://github.com/Khoert/Youtube_Guide/assets/140905959/6f625dbc-3ac1-4c42-be2b-553802620788


## Installation
1. Clone the repository   

+ Open Powershell and go to the location of your choice e.g. C:\Users\xyz
+ Clone the repository with the Powershell command "git clone https://github.com/Khoert/Youtube_Guide.git"

2. Installing   
+ In Powershell change to the installed repository, where requirements.txt is located
+ Install all packages required for the app with the Powershell command: "python -m pip install -r requirements.txt"

3. Add the API keys
+ Outside of Powershell open the file YT_guide_v2.py of the installed repository with e.g. a text editor
+ Add the Anyscale API key in line 28 of  script YT_guide_v2.py
+ Add the Youtube API key in line 38 of  script YT_guide_v2.py       

## Running the app in your web browser 
+ Go back to Powershell
+ Change to the location in the installed repository, where YT_guide_v2.py is located
+ Start the app in your web browser with the command "python -m streamlit run path/to/YT_guide_v2.py"
