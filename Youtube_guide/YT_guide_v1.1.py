####################################################
# import section
#######################################################
import streamlit as st
import os
from googleapiclient.discovery import build
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import pipeline
import time
from langchain.document_loaders import YoutubeLoader
import re    



####################################################
# intitialize
#######################################################

#youtube_key = os.environ.get('YOUTUBE_KEY')

####################################################
# define functions
#######################################################
      

def intitialize():
    global youtube_key, youtube, summarizer, prefix, summary_suffix
    youtube_key = "YOUR_YOUTUBE_API_KEY"
    youtube = build('youtube', 'v3', developerKey=youtube_key)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    prefix = 'https://www.youtube.com/watch?v='
    summary_suffix = "_summary.txt"


@st.cache
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


@st.cache 
def get_details(video_id):
    request = youtube.videos().list(
        id=video_id,
        part="snippet,contentDetails,statistics"
    )
    response = request.execute()
    return response


#list docs cannot be hased with the st.cache operation -> put underscore before var _docs
def token_count(docs):
    token_counts = [len(doc.page_content.split()) for doc in docs]
    total_token_ct = sum(token_counts)
    return total_token_ct, token_counts


# function to generate the summary
def get_summary(docs, token_counts, name):
    summary_all = ''
    text_all = ''
        
    # Check if summary file already exists
    project_folder = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the project folder
    folder_name = os.path.join(project_folder, "../Output")  # Create the output folder path
    os.makedirs(folder_name, exist_ok=True)  # Create the output folder if it doesn't exist
    file_name = os.path.join(folder_name, name)  # Create the file path
    if os.path.isfile(file_name):
        st.write("Summary file already exists:", file_name)
    else:
        bar = st.progress(0)
        st.write("There are " + str(len(docs)) + " snippets of the transcript to be processed." )
        for index, item in enumerate(docs):
            if index < len(docs):
                min_token = int(0.15*token_counts[index])
                max_token = int(0.3*token_counts[index])
                text_piece = docs[index].page_content
                text_all += text_piece
                summary_piece = summarizer(text_piece, max_length=max_token, min_length=min_token, do_sample=False)
                summary_text = summary_piece[0]['summary_text']
                summary_text = summary_text + ". "
                summary_all = summary_all + summary_text
                
                bar.progress((100//len(docs))*(index+1))
    return summary_all, text_all


# Function to save summary to a text file
def save_summary_to_file(name, summary):
    current_directory = os.getcwd()  # Get the current working directory
    folder_name = os.path.join(current_directory, "../Output")  # Create the output folder path
    os.makedirs(folder_name, exist_ok=True)  # Create the output folder if it doesn't exist
    file_name = os.path.join(folder_name, name)  # Create the file path
    
    if os.path.isfile(file_name):        
        print("Summary file already exists:", file_name)
    else:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(summary)
        st.write("Summary saved to:", file_name)


# Function to create header information of the summary file
def create_summary_header(current_title, current_v_length, current_url):
    info_1 = "This is a summary of the video with title: " + current_title + ". "
    info_2 = "The length of the video is: " + current_v_length + ". "
    info_3 = "The url of the video is: " + current_url + ". " 
    header_txt = info_1 + info_2 + info_3 + "_tt_ "     
    return header_txt

# Function to capitalize each letter in string
def capitalize_letters(string):
    capitalized_string = string.upper()
    return capitalized_string

  

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
        
        # Define text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,  # number of tokens overlap between chunks
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
            current_title_topic = f"{current_topic}_tt_"f"{current_title}"
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
            
            if current_caption_flag == 'true':
                # loading video transcription
                # add check if there is a transcript at all.
                loader = YoutubeLoader.from_youtube_url(current_url, add_video_info=True)
                loaded_video_trans = loader.load()
                current_docs = text_splitter.split_documents(loaded_video_trans)
                #st.write(current_docs[0].page_content)
                current_total_token_ct, current_token_counts = token_count(current_docs)
                st.write("The transcript has a total token count of: " + str(current_total_token_ct))
                st.markdown("""---""")
                                        
                # create a summary
                if os.path.isfile(current_summary_file_name):
                    st.write("Summary file already exists:", current_summary_file_name)
                else:
                    st.write("Start generating the summary.")            
                    start_time = time.time()
                    summary_all, text_all = get_summary(current_docs, current_token_counts, current_summary_file_name)
                    # stop the timer
                    end_time = time.time()
                    st.write("The summary of the video: " + current_title + " has been generated.")
                    # print the execution time
                    st.write("The execution time:", end_time - start_time, "seconds.")
                    
                    # saving the summary and full text file
                    summary_header = create_summary_header(current_title, current_v_length, current_url)
                    summary_all = summary_header + summary_all
                    text_all = summary_header + text_all
                    save_summary_to_file(current_summary_file_name, summary_all)    
                    save_summary_to_file(current_alltext_file_name, text_all)                       
                    st.markdown('<hr style="height:2px;border-width:0;color:gray;background-color:gray">', unsafe_allow_html=True)

            
            else:
                st.write("There is no transcription available for the video to create a summary") 

if __name__ == "__main__":
    main()