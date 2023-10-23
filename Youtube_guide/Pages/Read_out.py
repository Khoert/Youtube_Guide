

#%%###################################################
# import section
#######################################################

import os
import streamlit as st
from gtts import gTTS


#%%###################################################
# definition section
#######################################################


def extract_string_before_x(full_string):
    index = full_string.find('_x')
    if index != -1:
        return full_string[:index]
    else:
        return full_string

def extract_string_after_x(full_string):
    index = full_string.find("_x")
    if index != -1:
        return full_string[index + len("_x"):]
    else:
        return ""

def extract_string_before_mt(full_string):
    index = full_string.find('Main text:')
    if index != -1:
        return full_string[:index]
    else:
        return full_string
    
def extract_string_after_mt(full_string):
    index = full_string.find("Main text:")
    if index != -1:
        return full_string[index + len("Main text:"):]
    else:
        return ""
    

def get_files_with_substrings(directory, substring1, substring2):
    file_path_list = []
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if substring1 in file and substring2 in file:
                file_list.append(file)
                file_path_list.append(os.path.join(root, file))
    result_dict = dict(zip(file_list, file_path_list))
    return result_dict


def extract_topics_from_files(directory):
    file_list = os.listdir(directory)
    topics = set()  # Use a set to store unique topics
    for name in file_list:
        topic = extract_string_before_x(name)      
        topics.add(topic)  # Add the topic to the set      
    return list(topics)  # Convert the set back to a list


def load_text_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()
    return text


# Function to generate speech from text
def generate_speech(text):
    global audio_file, is_playing
    tts = gTTS(text, lang ='en-gb', slow=False)
    audio_file = "output.mp3"
    tts.save(audio_file)
    return audio_file


#%%###################################################
# selection section 
#######################################################

# test file selection
current_directory = os.getcwd()  # Get the current working directory
#st.write(current_directory)
folder_name = os.path.join(current_directory, "Output")  # Create the output folder path
#st.write(folder_name)


# get topic list
topic_list = extract_topics_from_files(folder_name)
print("Topics extracted from file names:")
# for topic in topic_list:
#     st.write(topic)


#%%###################################################
# main section 
#######################################################

file_extension = "_summary.txt"
topic_list.append("")


# Streamlit app code
def main():
    
    st.title("Summary read out")

    st.write("In this section you can choose an AI voice to read for you a selected summary file. "
             "The files are categorized by your search topics. "
             "On the left you must enter first the topic, then the a particular file related to the chosen topic. ")

    st.markdown('<hr style="height:2px;border-width:0;color:gray;background-color:gray">', unsafe_allow_html=True)
    
    if not topic_list:
        st.error("No files found in database. Please upload a file first.")
    else:
        # List of text files to choose from
        selected_topic = st.sidebar.selectbox("Select a topic:", topic_list)
        
        # given selected topic show all possible summary files to be chosen for review. 
        # get summary file list for a given topic
        summary_file_dic = get_files_with_substrings(folder_name,file_extension,selected_topic)
        summary_file_list = list(summary_file_dic.keys())
                                     
        # List of text files to choose from
        selected_file = st.sidebar.selectbox("Select a summary file from the topic:", summary_file_list)
        #st.write(selected_file)
        selected_file_path = summary_file_dic[selected_file]
              
        if not selected_file:
            st.error("Please select a file from the drop down menu or upload your first document")
        else:
        # Load text and additional information from selected file
            st.subheader(':blue[You have selected the topic]')
            st.write(selected_topic)
            
            st.subheader(':blue[The selected file is]')
            st.write(selected_file)
                   
             # Load the text file
            text = load_text_file(selected_file_path)
            video_text = extract_string_before_mt(text)
            audio_text = extract_string_after_mt(text)
            # Display the text box and allow editing
            #edited_text = st.text_area("This is the selected summary, that can be edited in the window", text)
            st.subheader(':blue[Vidoe infos]')
            st.write(video_text)
            st.subheader(':blue[Summary text]')
            st.write(audio_text)
            st.markdown('<style>textarea{height: 400px; width: 900px;}</style>', unsafe_allow_html=True)
            
            if st.button("Generate Speech"):
                if text:
                    audio_file = generate_speech(audio_text)
                    st.audio(audio_file)
                    
    
                        
                        
        
    

           
                
            
if __name__ == "__main__":
    main()
    



# %%
