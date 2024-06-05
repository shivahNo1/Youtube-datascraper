# YouTube Data Scraper

This project extracts data from YouTube related to a user-provided keyword. It includes video details and comments, then uploads the data to a MySQL database. The data is organized by creating a table with the keyword as its name.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Code Explanation](#codeexplanation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)


## Features

- Extract video data (title, channel, likes, dislikes, views) related to a specific keyword.
- Extract comments from the top 10 comments of each video.
- Upload the extracted data to a MySQL database.
- User-friendly interface using Streamlit.

## Prerequisites

Before running the application, ensure you have the following dependencies installed:

- Python 3.7+
- MySQL server
- Google Cloud Platform account with YouTube Data API enabled

## Installation

1. **Clone the repository**:
```sh
git clone <repository-url>
```

2. **Python Packages**:
```sh
pip install mysql-connector-python pandas google-api-python-client streamlit

```
3. **MySQL Database Setup**

- Ensure you have a MySQL database set up and running. Update the MySQL credentials in the script as needed.

4. **Google API Key**

- Obtain your YouTube Data API key from Google Cloud Platform and replace the placeholder in the script with your key.



## Usage

- Run the application:
 ```sh
streamlit run ticket_booking.py
 ```

- Input the keyword you want to search for in the Streamlit interface.
- Specify the number of videos you want to scrape.
- Click on "Extract Data" to fetch the data from YouTube.
- After data extraction, the data is displayed in a table format within the Streamlit interface.
- If the data extraction is successful, the data will be uploaded to your MySQL database.

## Screenshots

[Main page of scraper](https://github.com/shivahNo1/Youtube-datascraper/assets/171788487/a7e53b06-7c0e-4680-bad5-1762eaba94ab)


[same data scraping [output]](https://github.com/shivahNo1/Youtube-datascraper/assets/171788487/efbe5b90-c50f-4537-a6e6-cfc63571fe34)



## Code Explanation

- **Extract Data from YouTube**
The extract_data_from_youtube function initializes the YouTube Data API client and searches for videos related to the provided keyword. It retrieves video details and statistics, and fetches the top comments for each video.

- **Upload Data to MySQL**
The upload_to_mysql function connects to the MySQL database, creates a table (if it doesn't exist) using the keyword as the table name, and inserts the extracted data into this table.

- **Main Function**
The main function sets up the Streamlit interface, takes user input, triggers the data extraction, and handles the data upload to MySQL.

## Troubleshooting

- **Network Errors**: Ensure you have a stable internet connection.
- **API Errors**: Check your API key and ensure you have the correct permissions enabled.
- **Database Errors**: Verify your MySQL server is running and accessible with the provided credentials.


## Contributing

Contributions are welcome! If you have any suggestions, bug fixes, or feature enhancements, feel free to submit a pull request.
