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

Select the desired option from the sidebar: "Collect Data" to fetch data from YouTube channels or "Search Database" to search and retrieve data from the PostgreSQL database.

Follow the instructions in the Streamlit app to collect data or search the database.

Workflow
Data Collection: The fetch_youtube_data function fetches data from YouTube channels using the YouTube Data API.
Data Storage: The fetched data is stored in a PostgreSQL database using the store_in_database function.
Search Database: Users can search and retrieve data from the PostgreSQL database using the Streamlit app.
Contributing
Contributions are welcome! Please follow these guidelines when contributing:

**CODE  **
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

3. Delete data
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




