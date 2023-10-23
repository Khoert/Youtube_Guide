####################################################
# Version using Llama 2
#######################################################

####################################################
# import section
#######################################################
import streamlit as st
import os
from googleapiclient.discovery import build
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
from langchain.document_loaders import YoutubeLoader
import re    
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import json


####################################################
# intitialize
#######################################################

#youtube_key = os.environ.get('YOUTUBE_KEY')

# Set LLM API base URL and API key
API_BASE = "https://api.endpoints.anyscale.com/v1"
API_KEY = "esecret_yupqgp23833hrh8q3rlih45gmz"


####################################################
# define functions
#######################################################
      

def intitialize():
    global youtube_key, youtube, summarizer, prefix, summary_suffix
    youtube_key = "AIzaSyC5zU3GYH3lCt0VnManA_IqTto4XHseqF0"
    youtube = build('youtube', 'v3', developerKey=youtube_key)
    prefix = 'https://www.youtube.com/watch?v='
    summary_suffix = "_summary.txt"
    

@st.cache_data
def perform_query(query, by_date=False, num_results=3):
    # this function gets a list of youtube videos based on the given query 
    if by_date:
        request = youtube.search().list(
                                        part="snippet",
                                        q=query,
                                        maxResults=num_results,
                                        order='date',
                                        type='video',
                                        relevanceLanguage = 'en'
                                    )
        response = request.execute()
    else:
        request = youtube.search().list(
                                        part="snippet",
                                        q=query,
                                        maxResults=num_results,
                                        order='viewCount',
                                        type='video',
                                        relevanceLanguage = 'en'
                                    )
        response = request.execute()

    return response


@st.cache_data
def get_details(video_id):
    request = youtube.videos().list(
        id=video_id,
        part="snippet,contentDetails,statistics"
    )
    response = request.execute()
    return response


@st.cache_data
def llama_summarizer(txt):
    prompt = "Can you summarize the following video transacript with max 25 percent of its length: \n" + txt
    
    # Create the request headers
    headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
    }
    # Create the request body
    body = {
    "model": "meta-llama/Llama-2-70b-chat-hf",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.7
    }
    # Make the POST request
    response = requests.post(
    f"{API_BASE}/chat/completions",
    headers=headers,
    json=body)    
    return response

@st.cache_data
def llama_retrieve_string_response(bytes_output):
  """Retrieves the string response in the "content" ignoring the bullet points.

  Args:
    bytes_output: The bytes output from the text generation launcher.

  Returns:
    A string containing the string response in the "content" ignoring the bullet points.
  """

  # Decode the bytes output to a string.
  string_output = bytes_output.decode()

  # Use a JSON parser to parse the string into a JSON object.
  json_object = json.loads(string_output)

  # Get the `content` field from the JSON object.
  content = json_object["choices"][0]["message"]["content"]
  
  # Remove the prefix.
  content = content[content.find(":") + 1:]

  return content

# function to generate the summary
def llama_get_summary(docs, name):
    summary_all = ''
        
    # Check if summary file already exists
    project_folder = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the project folder
    folder_name = os.path.join(project_folder, "Output")
    file_name = os.path.join(folder_name, name)  # Create the file path
    if os.path.isfile(file_name):
        #st.write("Summary file already exists:", file_name)
        print("Summary file already exists:", file_name) 
    else:
        bar = st.progress(0)
        st.write("There are " + str(len(docs)) + " snippets of the transcript to be processed." )
        for index, item in enumerate(docs):
            if index < len(item):
                response = llama_summarizer(item)
                summary_text = llama_retrieve_string_response(response.content)
                summary_all = summary_all + summary_text
                                
                bar.progress((100//len(docs))*(index+1))
    return summary_all


# Function to save summary to a text file
@st.cache_data
def save_summary_to_file(name, summary):
    project_folder = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the project folder
    folder_name = os.path.join(project_folder, "Output")  
    os.makedirs(folder_name, exist_ok=True)  # Create the output folder if it doesn't exist
    file_name = os.path.join(folder_name, name)  # Create the file path
    
    if os.path.isfile(file_name):        
        print("File already exists:", file_name)
    else:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(summary)
        st.write("File saved to:", file_name)


# Function to create header information of the summary file
@st.cache_data
def create_summary_header(current_title, current_v_length, current_url):
    info_1 = "This is a summary of the video with title: " + current_title + ". "
    info_2 = "The length of the video is: " + current_v_length + ". "
    info_3 = "The url of the video is: " + current_url + ". " 
    header_txt = info_1 + info_2 + info_3 + " Main text: "     
    return header_txt

# Function to capitalize each letter in string
@st.cache_data
def capitalize_letters(string):
    capitalized_string = string.upper()
    return capitalized_string

# Function to join all transcript texts from youtube_transcript_api
@st.cache_data
def join_all_text_pieces(text_data):
  """Joins all text pieces in a list of dictionaries into a single string.

  Args:
    text_data: A list of dictionaries, where each dictionary contains a 'text' key.

  Returns:
    A single string containing all of the text pieces, joined together.
  """

  joined_text = ""
  for text_piece in text_data:
    joined_text += text_piece['text']

  return joined_text


# Streamlit app code
def main():
        
    result = ""
    
    intitialize()
            
    st.title("Youtube Guide")

    st.write("This app creates summaries of Youtube videos by the topic of your choice, given a transcript is available on Youtube. " 
             "In addition you can filter the topic by 'Most Views' or 'Date'. "
             "Note, each summary may take a few minutes. Consider this when choosing the number of search result you want to obtain. ")


    with st.form('input'):
        # Query input
        query = st.text_input("Enter topic of interest:")

        # Filtering options
        filter_options = ["Most Views", "Date"]
        selected_option = st.selectbox("Filter by:", filter_options)

        # Number of search results input
        num_results = st.number_input("Number of search results:", min_value=1, max_value=100, value=3)
        
        submit_button = st.form_submit_button(label="Search")

    ## Initialize result variable
    #result = ""

    # Perform query based on selected option
    if submit_button:
        
        if selected_option == "Most Views":
            result = perform_query(query, num_results=num_results)
        elif selected_option == "Date":
            result = perform_query(query, by_date=True, num_results=num_results)
        else:
            result = "Invalid option selected."
    

    
    st.markdown('<hr style="height:2px;border-width:0;color:gray;background-color:gray">', unsafe_allow_html=True)
          
    # Analyze results if not empty
    st.write("Query Result:")


    if result != "":
        
        # Define text splitter for Bert
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=3500,
            chunk_overlap=100,  # number of tokens overlap between chunks
            #separators=['\n\n', '\n', ' ', '']
        )
        
        # Define text splitter Llama
        llama_text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=3500,
            chunk_overlap=200,  # number of tokens overlap between chunks
            #separators=['\n\n', '\n', ' ', '']
        )
       
        current_topic = re.sub(r"[^\w\s]", "", query)  # Remove strange characters
        current_topic = capitalize_letters(current_topic)
        current_topic = current_topic.replace(" ", "_")
        
        # Loop through the search Youtube results and create the summary        
        for index, item in enumerate(result['items']):
            # getting video details
            current_vid = item['id']['videoId']
            current_url = prefix + current_vid
            current_title = item["snippet"]["title"]
            current_title = current_title.replace(" ", "_")
            current_title = re.sub(r"[^\w\s]", "", current_title)  # Remove strange characters
            current_title_topic = f"{current_topic}_x_"f"{current_title}"
            current_summary_file_name = f"{current_title_topic}_summary.txt"
            current_alltext_file_name = f"{current_title_topic}.txt"
            #current_description = item["snippet"]["description"]
            current_vid_details = get_details(current_vid)
            current_v_length = current_vid_details['items'][0]['contentDetails']['duration']
            current_caption_flag = current_vid_details['items'][0]['contentDetails']['caption']
                        
            # section to display some information to the user during the process
            st.write(str(index + 1) + ". video " + " has the title: " + current_title)
            st.write("It has the url: " + current_url)
            st.write("It's length is: " + current_v_length)
            # st.write(current_description)
            # st.write(current_vid_details)
                      
                                    
            # create a summary
            if os.path.isfile(current_summary_file_name):
                st.write("Summary file already exists:", current_summary_file_name)
            else:
                st.write("Start generating the summary.")
                start_time = time.time()
                
                try:
                    transcript = YouTubeTranscriptApi.get_transcript(current_vid)
                except Exception as e:
                    print("Error occurred while getting transcript: {}".format(e))
                    transcript = None

                if transcript is not None:
                    text_all = join_all_text_pieces(transcript)
                    # split for LLM into chunks
                    text_chunks = llama_text_splitter.split_text(text_all)
                    summary_all = llama_get_summary(text_chunks,current_summary_file_name)
                    # stop the timer
                    end_time = time.time()
                    st.write("The summary of the video: " + current_title + " has been generated.")
                    # print the execution time
                    st.write("The execution time:", end_time - start_time, "seconds.")
                    st.write("Summary: ")
                    st.write(summary_all)
                    # saving the summary and full text file
                    summary_header = create_summary_header(current_title, current_v_length, current_url)
                    summary_all = summary_header + summary_all
                    text_all = summary_header + text_all
                    st.write("The full transcript and the summary are saved to the following locations: ")
                    save_summary_to_file(current_alltext_file_name, text_all)   
                    save_summary_to_file(current_summary_file_name, summary_all)    
                    st.markdown('<hr style="height:2px;border-width:0;color:gray;background-color:gray">', unsafe_allow_html=True)
                
                else:
                    st.write("No transcript available for summarization. Please choose another video.")
  
          
 

if __name__ == "__main__":
    main()
