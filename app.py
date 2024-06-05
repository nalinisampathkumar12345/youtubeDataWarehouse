import streamlit as st
import psycopg2
from googleapiclient.discovery import build 

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

def store_playlist_data(playlist_data,channel_id, db_connection):
    with db_connection.cursor() as cursor:
        for item in playlist_data['items']:
            playlist_id = item['id']
            playlist_name = item['snippet']['title']
            

            cursor.execute(
                """
                INSERT INTO Play_List (playlist_id, playlist_name, channel_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (playlist_id) DO NOTHING
                """,
                (playlist_id, playlist_name, channel_id)
            )

# Function to store comment data in the database
def store_comment_data(comment_data, channel_id, db_connection):
    with db_connection.cursor() as cursor:
        for item in comment_data['items']:
            comment_id = item['id']
            # The video ID might not be directly under 'snippet', so let's check the structure
            if 'snippet' in item and 'videoId' in item['snippet']:
                video_id = item['snippet']['videoId']
            else:
                # Handle the case where the video ID is not found
                video_id = None

            comment_text = item['snippet'].get('textOriginal', '')
            commenter_author = item['snippet'].get('authorDisplayName','')
            comment_published_date = item['snippet']['publishedAt']

            cursor.execute(
                """
                INSERT INTO Comment_details (comment_id, video_id, comment_text, commenter_author, comment_published_date)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (comment_id) DO NOTHING
                """,
                (comment_id, video_id, comment_text, commenter_author, comment_published_date)
            )

# Function to store video data in the database
def store_video_data(video_data, channel_id, db_connection):
    with db_connection.cursor() as cursor:
        for item in video_data['items']:
            video_id = item['id']
            video_title = item['snippet']['title']
            video_description = item['snippet']['description']
            published_date = item['snippet']['publishedAt']
            views_count = item['statistics'].get('viewCount', 0)
            like_count = item['statistics'].get('likeCount', 0)
            dislikes_count = item['statistics'].get('dislikeCount', 0)
            favorite_count = item['statistics'].get('favoriteCount', 0)
            comment_count = item['statistics'].get('commentCount', 0)
            duration = item['contentDetails'].get('duration', 0)
            thumbnail = item['snippet']['thumbnails']['default']['url']
            caption_status = item['contentDetails'].get('caption', '')  # Handle missing 'caption' key

            cursor.execute(
                """
                INSERT INTO Video (video_id, video_title, video_description, published_date, views_count, like_count, dislikes_count,
                favorite_count, comment_count, duration, thumbnail, caption_status, channel_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (video_id) DO NOTHING
                """,
                (video_id, video_title, video_description, published_date, views_count, like_count, dislikes_count,
                favorite_count, comment_count, duration, thumbnail, caption_status, channel_id)
            )
# Function to store data in the database
def store_in_database(data, db_connection):
    with db_connection.cursor() as cursor:
        # Extract relevant data
        channel_id = data['items'][0]['id']
        channel_name = data['items'][0]['snippet']['title']
        
        # Check if 'channelType' key is present in the response
        if 'channelType' in data['items'][0]['snippet']:
            channel_type = data['items'][0]['snippet']['channelType']
        else:
            channel_type = None  # or set to a default value
        
        channel_view = data['items'][0]['statistics'].get('viewCount', 0)  # Handle if 'viewCount' key is missing
        channel_description = data['items'][0]['snippet'].get('description', '')  # Handle if 'description' key is missing
        
        # Check if 'status' key is present in the response
        if 'status' in data['items'][0]:
            channel_status = data['items'][0]['status'].get('privacyStatus', '')  # Handle if 'privacyStatus' key is missing
        else:
            channel_status = ''  # or set to a default value
        
        # Insert data into PostgreSQL table
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


    store_playlist_data(data,channel_id, db_connection)
    store_video_data(data,channel_id, db_connection)
    store_comment_data(data,channel_id, db_connection)
   
    db_connection.commit()


# Function to search and retrieve data from the database
def search_database(query, db_connection):
    # Implement logic to search and retrieve data from the database
    pass

def main():
    st.title("YouTube Data Harvesting and Warehousing")

    option = st.sidebar.selectbox("Select Option", ["Collect Data", "Search Database"])

    if option == "Collect Data":
        # User input for YouTube channel IDs
        channel_ids = st.text_input("Enter YouTube Channel IDs (separated by commas):")

        if st.button("Collect Data"):
            channel_ids = channel_ids.split(",")
            for channel_id in channel_ids:
                data = fetch_youtube_data(channel_id)
                # store_in_database(data, db_connection)

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
                # SQL query
                query = """
                    SELECT Video.video_title, Channel.channel_name
                    FROM Video
                    JOIN Channel ON Video.channel_id = Channel.channel_id;
                """
                # Execute the query and display results
                execute_and_display_query(query, db_connection)

            elif search_query == "Channels with the most number of videos":
                # SQL query
                query = """
                    SELECT Channel.channel_name, COUNT(Video.video_id) AS num_videos
                    FROM Channel
                    JOIN Video ON Channel.channel_id = Video.channel_id
                    GROUP BY Channel.channel_id
                    ORDER BY num_videos DESC
                    LIMIT 1;
                """
                # Execute the query and display results
                execute_and_display_query(query, db_connection)

            elif search_query == "Top 10 most viewed videos and their respective channels":
                # SQL query
                query = """
                    SELECT Video.video_title, Video.views_count, Channel.channel_name
                    FROM Video
                    JOIN Channel ON Video.channel_id = Channel.channel_id
                    ORDER BY Video.views_count DESC
                    LIMIT 10;
                """
                # Execute the query and display results
                execute_and_display_query(query, db_connection)

            elif search_query == "Number of comments on each video and their corresponding names":
                # SQL query
                query = """
                    SELECT Video.video_title, COUNT(Comment_details.comment_id) AS num_comments
                    FROM Video
                    LEFT JOIN Comment_details ON Video.video_id = Comment_details.video_id
                    GROUP BY Video.video_id;
                """
                # Execute the query and display results
                execute_and_display_query(query, db_connection)

            elif search_query == "Videos with the highest number of likes and their corresponding channel names":
                # SQL query
                query = """
                    SELECT Video.video_title, Video.like_count, Channel.channel_name
                    FROM Video
                    JOIN Channel ON Video.channel_id = Channel.channel_id
                    ORDER BY Video.like_count DESC
                    LIMIT 1;
                """
                # Execute the query and display results
                execute_and_display_query(query, db_connection)

            elif search_query == "Total number of likes and dislikes for each video and their corresponding names":
                # SQL query
                query = """
                    SELECT Video.video_title, Video.like_count, Video.dislikes_count
                    FROM Video;
                """
                # Execute the query and display results
                execute_and_display_query(query, db_connection)

            elif search_query == "Total number of views for each channel and their corresponding names":
                # SQL query
                query = """
                    SELECT Channel.channel_name, SUM(Video.views_count) AS total_views
                    FROM Channel
                    JOIN Video ON Channel.channel_id = Video.channel_id
                    GROUP BY Channel.channel_id;
                """
                # Execute the query and display results
                execute_and_display_query(query, db_connection)
            elif search_query == "Channels that have published videos in 2022":
                # SQL query
                query = """
                    SELECT DISTINCT Channel.channel_name
                    FROM Channel
                    JOIN Video ON Channel.channel_id = Video.channel_id
                    WHERE EXTRACT(YEAR FROM Video.published_date) = 2022;
                """
                # Execute the query and display results
                execute_and_display_query(query, db_connection)

            elif search_query == "Average duration of all videos in each channel and their corresponding names":
                # SQL query
                query = """
                     SELECT Channel.channel_name, AVG(Video.duration) AS avg_duration
                     FROM Channel
                     JOIN Video ON Channel.channel_id = Video.channel_id
                     GROUP BY Channel.channel_id;
                """
                # Execute the query and display results
                execute_and_display_query(query, db_connection)

            elif search_query == "Videos with the highest number of comments and their corresponding channel names":
                # SQL query
                query = """
                     SELECT Video.video_title, Video.comment_count, Channel.channel_name
                     FROM Video
                     JOIN Channel ON Video.channel_id = Channel.channel_id
                     ORDER BY Video.comment_count DESC
                     LIMIT 1;
                """
                # Execute the query and display results
                execute_and_display_query(query, db_connection)

# Function to execute SQL query and display results
def execute_and_display_query(query, db_connection):
    with db_connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        # Display results
        for row in results:
            st.write(row)

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