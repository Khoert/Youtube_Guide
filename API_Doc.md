## YouTube Guide Summarizer API Documentation
### Introduction
```shell
The YouTube Guide Summarizer is a Python script that creates summaries of YouTube videos by the topic of your choice,
provided a transcript is available on YouTube. To use this script, you need to obtain a YouTube API key,
which is required for accessing the YouTube Data API.
```
### Getting a YouTube API Key
```shell
To obtain a YouTube API key, you need to follow these steps:

1. Create a Google Cloud Project:
  - Go to the Google Cloud Console: https://console.cloud.google.com/
  - Sign in with your Google Account or create a new account if you don't have one.
  - Click on the project dropdown and select "New Project"
  - Enter a unique name for your project, choose a billing account (if required), and click on "Create."

2. Enable the YouTube Data API:
  - In the Google Cloud Console, navigate to "APIs & Services" > "Library."
  - Search for "YouTube Data API" and click on it.
  - Click on the "Enable" button to enable the API for your project.

3. Create Credentials:
  - In the Google Cloud Console, navigate to "APIs & Services" > "Credentials."
  - Click on the "Create credentials" button and select "API key."
  - A new API key will be generated. Copy the API key and save it securely.

4. Restrict the API Key (Optional):
  - For security purposes, it is recommended to restrict the usage of your API key to only the services you need.
    You can do this by setting up API restrictions in the Credentials section of the Google Cloud Console.
```

### Using the YouTube API Key in the Script
```shell
Once you have obtained your YouTube API key, you need to add it to the Python script (YT_guide_v1.1.py)
in the intitialize() function.

Replace "YOUTUBE_KEY" with your actual YouTube API key. With this change,
the script will be able to access the YouTube Data API and retrieve video information for summarization.
```

