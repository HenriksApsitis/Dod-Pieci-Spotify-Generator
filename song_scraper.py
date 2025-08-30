from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from urllib.parse import urljoin

base_url = "https://dod.pieci.lv/dziesmu-mekletajs"
url = base_url
song_list = []
count = 0
while url:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')  # Parse html data
        # print(soup.prettify())
        table = soup.find('table') # Find first table
        rows_data = soup.find_all('tr') # Find all rows
        for row in rows_data:
            separated_row_data = row.find_all('td') # Seperate data on td tags
            if len(separated_row_data) > 0:
                data = [table_data.get_text(strip=True) for table_data in separated_row_data]
                formatted_song = re.sub(r'\s*-\s*', ' - ', data[0])
                song_list.append(formatted_song)
                count += 1
                print('Found ',count, 'song(s)')

        next_li = soup.find("li", class_="page-item next")
        if next_li:
            next_link = next_li.find("a")
            url = urljoin(base_url, next_link["href"]) if next_link else None
        else:
            url = None  # stop if no next page
    else:
        print("Failed to retrieve page:", response.status_code)
if song_list:
    print(song_list)
    unique_songs = list(dict.fromkeys(song_list))
    print(count, "songs found")
    df = pd.DataFrame({"Song": unique_songs})
    df.index = df.index + 1
    df.index.name = "No."
    print(df)
    df.to_csv("songs.csv")



