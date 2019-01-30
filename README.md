# pubg_time_series_stats

This script allows you to get PUBG player data via API.

It will:
* Iterate through a player's games.
* Put all data into a Pandas DataFrame
* Store the data locally in a CSV file
* You can open the CSV and maniuplate it however you want (Excel, Pandas, etc.)

Currently There are Hardcoded Values:
* NA Shard Results
* Playername for looking up
* Wait time delay between API requests.
