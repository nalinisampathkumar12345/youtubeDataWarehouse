import streamlit as st
import psycopg2
import pandas as pd
import re
import isodate
from googleapiclient.discovery import build 




st.markdown("""
    <style>
    .title {
        text-align: center;
        color: #FF5733;  /* You can change this color */
        font-size: 35px;
        font-weight: bold;
    }
    </style>
    <h1 class="title">YouTube Data Harvesting and Warehousing</h1>
    """, unsafe_allow_html=True)

def main():
   
    option = st.sidebar.selectbox("Select Option", ["Collect Data", "Search Database",])

    if option == "Collect Data":
        # User input for YouTube channel IDs
        channel_ids = st.text_input("Enter YouTube Channel IDs (separated by commas):")

        if st.button("Collect Data"):
            if channel_ids:
              channel_ids = channel_ids.split(",")
            else:
              st.error("Please provide channel IDs")   
            for channel_id in channel_ids:
                data = fetch_youtube_data(channel_id)
                store_in_database(data, db_connection)
                
            st.success("Data stored successfully!")
    
        if st.button("Clean"):
           clean_data(db_connection)
           st.success("Data cleaning and processed successfully!")

        if st.button("Delete"):
           delete_data(db_connection)
           st.success("Data deleted successfully!")

    elif option == "Search Database":
        # User input for search query
        # Dropdown menu for selecting the query type
        search_query = st.selectbox(
            "Select Query Type",
            [
                "Names of all videos and their corresponding channels",
                "Channels with the most number of videos",
                "Top 10 most viewed videos and their respective channels",
                "Number of comments on each video and their corresponding names",
                "Videos with the highest number of likes and their corresponding channel names",
                "Total number of likes and dislikes for each video and their corresponding names",
                "Total number of views for each channel and their corresponding names",
                "Channels that have published videos in 2022",
                "Average duration of all videos in each channel and their corresponding names",
                "Videos with the highest number of comments and their corresponding channel names",
            ]
        )
        
        if st.button("Search"):
            results = search_database(search_query, db_connection)
            # Display search results
            if search_query == "Names of all videos and their corresponding channels":
                
                query = """
                    SELECT Video.video_title, Channel.channel_name
                    FROM Video
                    JOIN Channel ON Video.channel_id = Channel.channel_id;
                """
                execute_and_display_query(query, db_connection)

            elif search_query == "Channels with the most number of videos":
               
                query = """
                    SELECT Channel.channel_name, COUNT(Video.video_id) AS num_videos
                    FROM Channel
                    JOIN Video ON Channel.channel_id = Video.channel_id
                    GROUP BY Channel.channel_id
                    ORDER BY num_videos DESC
                    LIMIT 1;
                """
                
                execute_and_display_query(query, db_connection)

            elif search_query == "Top 10 most viewed videos and their respective channels":
               
                query = """
                    SELECT Video.video_title, Video.views_count, Channel.channel_name
                    FROM Video
                    JOIN Channel ON Video.channel_id = Channel.channel_id
                    ORDER BY Video.views_count DESC
                    LIMIT 10;
                """
             
                execute_and_display_query(query, db_connection)

            elif search_query == "Number of comments on each video and their corresponding names":
                
                query = """
                    SELECT Video.video_title, COUNT(Comment_details.comment_id) AS num_comments
                    FROM Video
                    LEFT JOIN Comment_details ON Video.video_id = Comment_details.video_id
                    GROUP BY Video.video_id;
                """
                
                execute_and_display_query(query, db_connection)

            elif search_query == "Videos with the highest number of likes and their corresponding channel names":
                
                query = """
                    SELECT Video.video_title, Video.like_count, Channel.channel_name
                    FROM Video
                    JOIN Channel ON Video.channel_id = Channel.channel_id
                    ORDER BY Video.like_count DESC
                    LIMIT 1;
                """
                
                execute_and_display_query(query, db_connection)

            elif search_query == "Total number of likes and dislikes for each video and their corresponding names":
               
                query = """
                    SELECT Video.video_title, Video.like_count, Video.dislikes_count
                    FROM Video;
                """
               
                execute_and_display_query(query, db_connection)

            elif search_query == "Total number of views for each channel and their corresponding names":
                
                query = """
                    SELECT Channel.channel_name, SUM(Video.views_count) AS total_views
                    FROM Channel
                    JOIN Video ON Channel.channel_id = Video.channel_id
                    GROUP BY Channel.channel_id;
                """
                
                execute_and_display_query(query, db_connection)
            elif search_query == "Channels that have published videos in 2022":
               
                query = """
                    SELECT DISTINCT Channel.channel_name
                    FROM Channel
                    JOIN Video ON Channel.channel_id = Video.channel_id
                    WHERE EXTRACT(YEAR FROM Video.published_date) = 2022;
                """
               
                execute_and_display_query(query, db_connection)

            elif search_query == "Average duration of all videos in each channel and their corresponding names":
                
                query = """
                     SELECT Channel.channel_name, AVG(Video.duration) AS avg_duration
                     FROM Channel
                     JOIN Video ON Channel.channel_id = Video.channel_id
                     GROUP BY Channel.channel_id;
                """
               
                execute_and_display_query(query, db_connection)

            elif search_query == "Videos with the highest number of comments and their corresponding channel names":
               
                query = """
                     SELECT Video.video_title, Video.comment_count, Channel.channel_name
                     FROM Video
                     JOIN Channel ON Video.channel_id = Channel.channel_id
                     ORDER BY Video.comment_count DESC
                     LIMIT 1;
                """
                
                execute_and_display_query(query, db_connection)


# Function to fetch data from YouTube Data API

def fetch_youtube_data(channel_id):
    # Initialize YouTube API
    youtube = build('youtube', 'v3', developerKey='AIzaSyDeUgn72K5XTlJpo3iDFZCckaWsVOdgoRE')
    
    # Fetch channel data
    request = youtube.channels().list(
        part="snippet,statistics,contentDetails",
        id=channel_id
    )
    response = request.execute()
    return response



def fetch_playlist_info(channel_id):
    try:
       
        channelID = channel_id['id']
        #st.success(channelID)

        youtube = build('youtube', 'v3', developerKey='AIzaSyDeUgn72K5XTlJpo3iDFZCckaWsVOdgoRE')
        request = youtube.playlists().list(
            part="snippet",
            channelId=channelID
        )
        response = request.execute()
        playlist = []
        #st.success(response)
        for item in response.get('items', []):
            playlist_id = item['id']
            playlist_name = item['snippet']['title']
            playlist.append({'playlist_id': playlist_id, 'title': playlist_name})
        
        return playlist
      
    except Exception as e:
        print(f"Error fetching playlist information: {e}")
        return None

def fetch_comments_for_video(video_id):
    try:
       
        youtube = build('youtube', 'v3', developerKey='AIzaSyDeUgn72K5XTlJpo3iDFZCckaWsVOdgoRE')
        request = youtube.commentThreads().list(
           part="snippet",
           videoId=video_id,
           maxResults=5
         )
        response = request.execute()
        #st.success(response)
        return response
      
    except Exception as e:
        print(f"Error fetching videoList information: {e}")
        return None


def store_comment_data(comment_data, video_id, db_connection, cursor):
    if comment_data and 'items' in comment_data:
        for item in comment_data['items']:
            comment_id = item['id']
            snippet = item.get('snippet', {}).get('topLevelComment', {}).get('snippet', {})
            comment_text = snippet.get('textOriginal', '')
            commenter_author = snippet.get('authorDisplayName', '')
            comment_published_date = snippet.get('publishedAt', '')


            cursor.execute(
                """
                INSERT INTO Comment_details (comment_id, video_id, comment_text, commenter_author, comment_published_date)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (comment_id) DO NOTHING
                """,
                (comment_id, video_id, comment_text, commenter_author, comment_published_date)
            )
    else:
        print(f"No comments found for video {video_id}")

# Function to store playlist data from YouTube Data API
def store_playlist_data(playlist_info, channel_id, db_connection, cursor):
    query = """
        INSERT INTO Play_List (playlist_id, playlist_name, channel_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (playlist_id) DO NOTHING
    """
    if playlist_info:
        #st.success(playlist_info)
        for item in playlist_info:
            playlist_id = item.get('playlist_id')
            playlist_name = item.get('title', 'Unknown Playlist')
            cursor.execute(query, (playlist_id, playlist_name, channel_id))
            videolist = fetch_videos_for_playlist(playlist_id)
            store_video_data(videolist, channel_id, db_connection, cursor)
    else:
        print("No playlist information provided.")


def fetch_videos_statistics(video_ids):
    youtube = build('youtube', 'v3', developerKey='AIzaSyDeUgn72K5XTlJpo3iDFZCckaWsVOdgoRE')
    statistics = []

    request = youtube.videos().list(
        part="statistics,contentDetails",
        id=",".join(video_ids)
    )
    response = request.execute()
    for item in response.get('items', []):
        stats = item.get('statistics', {})
        content_details = item.get('contentDetails', {})
        #st.success(content_details)
        stats['duration'] = content_details.get('duration', 0)
        #t.success(stats)
        statistics.append(stats)

    return statistics


# Function to store playlist data from YouTube Data API
def fetch_videos_for_playlist(playlist_id):
    if isinstance(playlist_id, str):
        playListID = playlist_id
        #st.success(playListID)
        youtube = build('youtube', 'v3', developerKey='AIzaSyDeUgn72K5XTlJpo3iDFZCckaWsVOdgoRE')
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playListID,
            maxResults=5
        )
        response = request.execute()
        #st.success(response)
        return response
    elif isinstance(playlist_id, dict):
        playListID = playlist_id.get('id')
        #st.success(playListID)
        youtube = build('youtube', 'v3', developerKey='AIzaSyDeUgn72K5XTlJpo3iDFZCckaWsVOdgoRE')
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playListID,
            maxResults=5
        )
        response = request.execute()
        #st.success(response)
        return response
    else:
        st.error("Invalid playlist ID format. Expected string or dictionary.")
        return None


def store_video_data(video_data, channel_id, db_connection, cursor):
    video_ids = [item['contentDetails']['videoId'] for item in video_data.get('items', [])]
    video_statistics = fetch_videos_statistics(video_ids)

    for item, stats in zip(video_data.get('items', []), video_statistics):
        if isinstance(item, dict):
            content_details = item.get('contentDetails', {})
            snippet = item.get('snippet', {})
            #st.success(content_details)
            video_id = content_details.get('videoId', '')
            video_title = snippet.get('title', '')
            video_description = snippet.get('description', '')
            published_date = snippet.get('publishedAt', '')
            views_count = stats.get('viewCount', 0)
            like_count = stats.get('likeCount', 0)
            dislikes_count = stats.get('dislikeCount', 0)
            favorite_count = stats.get('favoriteCount', 0)
            comment_count = stats.get('commentCount', 0)
            
            iso_duration = stats.get('duration', 'PT0S')
            if not isinstance(iso_duration, str):
              iso_duration = 'PT0S'
            duration = int(isodate.parse_duration(iso_duration).total_seconds())  # Convert to seconds
            thumbnail = snippet.get('thumbnails', {}).get('default', {}).get('url', '')
            caption_status = content_details.get('caption', '')

            cursor.execute(
                """
                INSERT INTO Video (video_id, video_title, video_description, published_date, views_count, like_count,
                dislikes_count, favorite_count, comment_count, duration, thumbnail, caption_status, channel_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (video_id) DO NOTHING
                """,
                (video_id, video_title, video_description, published_date, views_count, like_count, dislikes_count,
                 favorite_count, comment_count, duration, thumbnail, caption_status, channel_id)
            )
            
            comments = fetch_comments_for_video(video_id)
            store_comment_data(comments, video_id, db_connection, cursor)


def store_in_database(data, db_connection):
    with db_connection.cursor() as cursor:
        for channel in data['items']:
            channel_id = channel['id']
            channel_name = channel['snippet']['title']
            channel_type = channel['snippet'].get('channelType')
            channel_view = channel['statistics'].get('viewCount', 0)
            channel_description = channel['snippet'].get('description', '')
            channel_status = channel.get('status', {}).get('privacyStatus', '')

            # Insert channel data
            cursor.execute(
                """
                INSERT INTO Channel (channel_id, channel_name, channel_type, channel_view, channel_description, channel_status)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (channel_id) DO UPDATE
                SET channel_name = EXCLUDED.channel_name,
                    channel_type = EXCLUDED.channel_type,
                    channel_view = EXCLUDED.channel_view,
                    channel_description = EXCLUDED.channel_description,
                    channel_status = EXCLUDED.channel_status
                """,
                (channel_id, channel_name, channel_type, channel_view, channel_description, channel_status)
            )
            #st.success(channel)
            channel_playlists = fetch_playlist_info(channel) 
            #st.success(channel_playlists)
            store_playlist_data(channel_playlists, channel_id, db_connection, cursor)
           
    db_connection.commit()

def search_database(query, db_connection):
    # Implement logic to search and retrieve data from the database
    pass


# Function to delete all data from the database
def delete_data(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute("DELETE FROM Comment_details")
        cursor.execute("DELETE FROM Video")
        cursor.execute("DELETE FROM Play_List")
        cursor.execute("DELETE FROM Channel")
    db_connection.commit()


def clean_data(db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE Channel
            SET channel_name = COALESCE(NULLIF(channel_name, ''), 'NA'),
                channel_type = COALESCE(NULLIF(channel_type, ''), 'NA'),
                channel_description = COALESCE(NULLIF(channel_description, ''), 'NA'),
                channel_status = COALESCE(NULLIF(channel_status, ''), 'NA');
            
            UPDATE Play_List
            SET playlist_name = COALESCE(NULLIF(playlist_name, ''), 'NA');
            
            UPDATE Comment_details
            SET comment_text = COALESCE(NULLIF(comment_text, ''), 'NA'),
                commenter_author = COALESCE(NULLIF(commenter_author, ''), 'NA');
            
            UPDATE Video
            SET video_title = COALESCE(NULLIF(video_title, ''), 'NA'),
                video_description = COALESCE(NULLIF(video_description, ''), 'NA'),
                thumbnail = COALESCE(NULLIF(thumbnail, ''), 'NA'),
                caption_status = COALESCE(NULLIF(caption_status, ''), 'NA');
            """
        )
    db_connection.commit()


# Function to execute SQL query and display results
def execute_and_display_query(query, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Fetch the column names
        colnames = [desc[0] for desc in cursor.description]
        
        # Convert the results to a DataFrame
        df = pd.DataFrame(results, columns=colnames)
        
        # Display the DataFrame in a table
        st.table(df)

# Connect to the database
db_connection = psycopg2.connect(
    host="aimlhost",
    port="5432",
    database="postgres",
    user="postgres",
    password="postgres@12345"
)

# Run the Streamlit app
if __name__ == "__main__":
    main()

# Footer
st.sidebar.write("Project by Nalini")
