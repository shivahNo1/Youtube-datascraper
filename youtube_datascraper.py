import mysql.connector as sql
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st

# YouTube API key
API_KEY = "APIKEY"

def extract_data_from_youtube(api_key, keyword, max_results):
    # Initialize the YouTube Data API v3 client
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Example: Getting top 'max_results' videos related to the keyword
    request = youtube.search().list(
        q=keyword,
        part="snippet",
        type="video",
        maxResults=max_results
    )
    response = request.execute()

    video_data = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        video_channel = item['snippet']['channelTitle']
        
        try:
            # Get video statistics (likes, dislikes, views)
            stats_request = youtube.videos().list(
                part="statistics",
                id=video_id
            )
            stats_response = stats_request.execute()
            statistics = stats_response['items'][0]['statistics']
            
            likes = statistics.get('likeCount', 0)
            dislikes = statistics.get('dislikeCount', 0)
            views = statistics.get('viewCount', 0)
            
            # Get video comments
            comments_request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=10
            )
            comments_response = comments_request.execute()
            comments = [comment['snippet']['topLevelComment']['snippet']['textDisplay'] for comment in comments_response['items']]
        except HttpError as e:
            if e.resp.status == 403:
                # Comments are disabled for this video, continue to the next video
                continue
            else:
                # Handle other HTTP errors
                raise
        
        video_data.append({
            'Video ID': video_id,
            'Title': video_title,
            'Channel': video_channel,
            'Likes': likes,
            'Dislikes': dislikes,
            'Views': views,
            'Comments': comments
        })

    return video_data


def upload_to_mysql(data, host, user, password, database, keyword):
    mydb = sql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    mycursor = mydb.cursor()

    # Create table if not exists
    table_name = f"{keyword.replace(' ', '_')}_data"  # Replace spaces with underscores
    create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\
                            `VideoID` VARCHAR(255) PRIMARY KEY, \
                            `Title` VARCHAR(255), \
                            `Channel` VARCHAR(255), \
                            `Likes` INT, \
                            `Dislikes` INT, \
                            `Views` INT, \
                            `Comments` TEXT\
                        )"
    mycursor.execute(create_table_query)

    # Insert data into the table
    insert_query = f"INSERT IGNORE INTO `{table_name}` (VideoID, Title, Channel, Likes, Dislikes, Views, Comments) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    for video in data:
        mycursor.execute(insert_query, (
            video['Video ID'],
            video['Title'],
            video['Channel'],
            video['Likes'],
            video['Dislikes'],
            video['Views'],
            ', '.join(video['Comments'])
        ))
    mydb.commit()
    print("Data uploaded to MySQL successfully.")


def main():
    # MySQL credentials
    host = 'localhost'
    user = 'root'
    password = ''
    database = 'youtube_data'

    st.title("YOUTUBE DATA SCRAPER")
    st.info("This project extracts data from YouTube related to a user-provided keyword, including video details and comments, then uploads it to MySQL, organizing the data by creating a table with the keyword as its name.")

    keyword = st.text_input("Keyword: ")

    max_videos = st.number_input("How many videos do you want to scrape?", min_value=1, max_value=50, value=10)

    data_uploaded = False  # Track whether data has been uploaded to the database
    
    # Add a button to trigger data extraction
    if st.button("Extract Data"):
        try:
            # Extracting data from YouTube
            youtube_data = extract_data_from_youtube(API_KEY, keyword, max_videos)
            st.success("Data is sucessfully extracted")
            # Display the table in the Streamlit UI
            df = pd.DataFrame(youtube_data)
            st.write(df)
        except:
            st.error("Network error! please contact the Administrator")

        data_uploaded = True  # Set to True after data extraction and display

    if data_uploaded:
        try:
            upload_to_mysql(youtube_data, host, user, password, database, keyword)
            st.success("Data successfully uploaded to Database")
            st.subheader("Thank you!")
        except:
            st.error("Database server is not working. please contact the Administrator")
       
        

          

main()

