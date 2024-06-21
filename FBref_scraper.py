# Import necessary libraries
from bs4 import BeautifulSoup  # Library for parsing HTML and XML documents
import pandas as pd            # Library for data manipulation and analysis
import requests                # Library for making HTTP requests
import time                    # Library for handling time-related tasks

# Initialize an empty list to store team data
all_teams = []

# Make an HTTP GET request to the URL and get the HTML content of the Premier League stats page
html = requests.get("https://fbref.com/en/comps/9/Premier-League-Stats").text

# Parse the HTML content using BeautifulSoup with lxml parser
soup = BeautifulSoup(html, "lxml")

# Find the first table with the class 'stats_table'
table = soup.find_all('table', class_='stats_table')[0]

# Extract all links within the table
links = table.find_all('a')
links = [l.get("href") for l in links]  # Get the href attribute of each link
links = [l for l in links if "/squads" in l]  # Filter links to include only those containing '/squads'

# Create full URLs for each team by concatenating with the base URL
team_urls = [f"https://fbref.com{l}" for l in links]

# Loop through each team URL to gather data
for team_url in team_urls:
    # Extract the team name from the URL
    team_name = team_url.split("/")[-1].replace("-Stats", "")
    
    # Make an HTTP GET request to the team URL and get the HTML content
    data = requests.get(team_url).text
    
    # Parse the HTML content using BeautifulSoup with lxml parser
    soup = BeautifulSoup(data, "lxml")
    
    # Find the first table with the class 'stats_table' on the team page
    stats = soup.find_all("table", class_="stats_table")[0]
    
    # If the stats table has a multi-level column index, drop the top level
    if stats and stats.columns:
        stats.columns = stats.columns.droplevel()
    
    # Convert the HTML table to a pandas DataFrame
    team_data = pd.read_html(str(stats))[0]
    
    # Add a new column 'Team' with the team name
    team_data["Team"] = team_name
    
    # Append the team's data to the all_teams list
    all_teams.append(team_data)
    
    # Pause for 5 seconds to avoid overwhelming the server with requests
    time.sleep(5)

# Concatenate all team DataFrames into a single DataFrame
stat_df = pd.concat(all_teams)

# Save the concatenated DataFrame to a CSV file
stat_df.to_csv("FBref_player_stats.csv")
