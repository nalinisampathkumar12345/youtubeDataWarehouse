YouTube Data Harvesting and Warehousing
This project aims to collect data from YouTube channels using the YouTube Data API and store it in a PostgreSQL database for further analysis.

pip install streamlit

**Installation**
**Clone the repository:**


git clone https://github.com/your-username/your-repository.git
cd your-repository

Set up PostgreSQL database:
Create a PostgreSQL database.
Update the database connection details in the code (main.py).
Usage
Run the Streamlit app:
streamlit run app.py
-------------------------------------------------------
**Apllication Cloning : https://github.com/nalinisampathkumar12345/youtubeDataWarehouse/blob/main/app.py**

**Sample Data :**
YoutubedataharvestingWarehouse
AIzaSyDeUgn72K5XTlJpo3iDFZCckaWsVOdgoRE - api key

UCsNxHPbaCWL1tKw2hxGQD6g, UCRzYN32xtBf3Yxsx5BvJWJw, UC3uJIdRFTGgLWrUziaHbzrg,UCY6KjrDBN_tIRFT_QNqQbRQ,UCBnZ16ahKA2DZ_T5W0FPUXg - channeled

UCI_mwTKUhicNzFrhm33MzBQ,UCqOxDZvr1uFgENnD1GJ9CVg,UChftTVI0QJmyXkajQYt2tiQ,UCcEb7YNDNBkU0hlrTjH7PfQ,UCVlWr_LN9y80smEMr0KTBOA

**Apllication Funcionality**
Select the desired option from the sidebar: "Collect Data" to fetch data from YouTube channels or "Search Database" to search and retrieve data from the PostgreSQL database.

Follow the instructions in the Streamlit app to collect data or search the database.

Workflow
Data Collection: The fetch_youtube_data function fetches data from YouTube channels using the YouTube Data API.
Data Storage: The fetched data is stored in a PostgreSQL database using the store_in_database function.
Search Database: Users can search and retrieve data from the PostgreSQL database using the Streamlit app.
Contributing
Contributions are welcome! Please follow these guidelines when contributing:

*CODE details*
19 methods created for the following 


I) Processing and  Managing Data
------------------------------

main()   - fetching data , store data in data base, search , clean , delete 

1 .Storing Data
--------------

store_in_database(data, db_connection):

store_comment_data(comment_data, video_id, db_connection, cursor):

store_playlist_data(playlist_info, channel_id, db_connection, cursor):

store_video_data(video_data, channel_id, db_connection, cursor):


2.** Search **
-------
search_database(query, db_connection):

**3. Delete data**
-------------
delete_data(db_connection):

4.** Processing Data**
--------------
clean_data(db_connection):

5**. Validating data **
-------------------

is_channel_id_exists(channel_id, db_connection) - Duplicate check 


**6. Fetch Data **
------------

fetch_youtube_data(channel_id)

fetch_playlist_info(channel_id)

fetch_comments_for_video(video_id):

fetch_videos_for_playlist(playlist_id):

fetch_videos_statistics(video_ids):


II)Table CRUD activity 
-----------------------

table_exists(cursor, table_name)

drop_table_if_exists(cursor, table_name):

drop_tables(db_connection):

create_tables_if_not_exist(db_connection)



III) Displaying the data in streamlit
----------------------------------

execute_and_display_query(query, db_connection):


-------------------------------------------------
**Table Script **

Table script 

CREATE TABLE Channel (
    channel_id VARCHAR(255) PRIMARY KEY,
    channel_name VARCHAR(255),
    channel_type VARCHAR(255),
    channel_view BIGINT,
    channel_description TEXT,+


    channel_status VARCHAR(255)
);

-- Table definition for Play_List
CREATE TABLE Play_List (
    playlist_id VARCHAR(255) PRIMARY KEY,
    channel_id VARCHAR(255),
    playlist_name VARCHAR(255),
    FOREIGN KEY (channel_id) REFERENCES Channel(channel_id) ON DELETE CASCADE
);

-- Table definition for Comment_details
CREATE TABLE Comment_details (
    comment_id VARCHAR(255) PRIMARY KEY,
    video_id VARCHAR(20),
    comment_text TEXT,
    commenter_author VARCHAR(255),
    comment_published_date TIMESTAMP,
    FOREIGN KEY (video_id) REFERENCES Video(video_id) ON DELETE CASCADE
);

CREATE TABLE Video (
    video_id VARCHAR(255) PRIMARY KEY,
    video_title VARCHAR(255),
    video_name VARCHAR(255),
    video_description TEXT,
    published_date TIMESTAMP,
    views_count BIGINT,
    like_count BIGINT,
    dislikes_count BIGINT,
    favorite_count BIGINT,
    comment_count BIGINT,
    duration INTEGER,
    thumbnail VARCHAR(255),
    caption_status VARCHAR(255),
    channel_id VARCHAR(255),  -- Foreign key referencing Channel table
    FOREIGN KEY (channel_id) REFERENCES Channel(channel_id) ON DELETE CASCADE
);


