
import os
from googleapiclient.discovery import build
import re
import pandas as pd
from sentiment_analysis import sentiment
import streamlit as st




api_key = st.secrets["YOUTUBE_API_KEY"]
def url_to_id(video_url):
    id =video_url.split('?v=')[1]
    if '&'in id:
        id = id.split('&')[0]
        
    return id
def fetch_comment_data(video_url):
    
    
    print('working')
    def clean_data(comment):
        if ('<' in comment) & ('>' in comment):
            comment = clean_tags(comment)
        return comment

        
    def clean_tags(comment):
        pattern = re.compile('<.*?>(.*</.*?>)?')
        text = re.sub(pattern, '', comment)
        return text

    


    video_id = url_to_id(video_url)
    comments = []
    youtube = build('youtube', 'v3', developerKey = api_key)
    
    video_response=youtube.commentThreads().list(
	    part='snippet',
	    videoId=video_id
	    ).execute()
    page = 1
    while video_response:
        
        for item in video_response['items']:
            comment = clean_data(item['snippet']['topLevelComment']['snippet']['textDisplay'])
            
            if comment != '':
                comments.append(comment)

        if 'nextPageToken' in video_response:
            print('page number: ',page)
            video_response=youtube.commentThreads().list(
	            part='snippet',
	            videoId=video_id,
                pageToken = video_response['nextPageToken']
	        ).execute()
            page += 1
        else:
            break
    data = pd.DataFrame({'comments':comments})
    print(len(comments), 'comments')
    return data

