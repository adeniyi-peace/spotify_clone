from bs4 import BeautifulSoup
import requests



def spotify_webscrapper():
    html_content = requests.get('https://open.spotify.com')

    soup = BeautifulSoup(html_content.content, 'html.parser').body
    divs = soup.find_all('div', class_='Box__BoxComponent-sc-y4nds-0')

    artists_data = []
    albums_data = []

    try:
        

        for items in divs:

            # Scrape popular artist data

            if "artist" in items["aria-labelledby"] and len(artists_data)<=9:
                artist_image_url=  items.find("img")["src"]
                artist_name = items.find("a").string
                artist_id = items.find("a")["href"].split('/')[-1]

                artists_data.append({
                    'artist_name': artist_name,
                    'artist_id': artist_id,
                    'artist_image_url': artist_image_url
                })

            # Scrape popular album data

            elif "album" in items["aria-labelledby"] and len(albums_data)<=9:
                album_image_url =  items.find("img")["src"]
                album_name = items.find("a").string
                album_id = items.find("a")["href"].split('/')[-1]

                request_artist = requests.get("https://open.spotify.com/album/" + album_id)
                scraped_data = BeautifulSoup(request_artist.content, "html.parser")
                details = scraped_data.find("div", attrs={"class":"e-9541-text encore-text-body-small b81TNrTkVyPCOH0aDdLG"})

                album_artist_id = details.find("a")["href"].split('/')[-1]
                album_artist = details.find("a").string
                        
                albums_data.append({
                    "album_id": album_id,
                    'album_name': album_name,
                    'album_image_url': album_image_url,
                    "album_artist_id": album_artist_id,
                    "album_artist": album_artist
                })
        return artists_data, albums_data

    except Exception as e:
        print(f"Error scraping spotify data: {e}")




