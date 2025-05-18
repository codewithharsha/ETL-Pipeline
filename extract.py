import requests
url = "https://raw.githubusercontent.com/codewithharsha/ETL-Pipeline/main/Border_Crossing_Entry_Data.csv"
response = requests.get(url)
with open("Border_Crossing_Entry_Data.csv", "wb") as f:
    f.write(response.content)
print("Download complete.")