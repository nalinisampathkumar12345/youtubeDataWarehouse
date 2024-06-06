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



