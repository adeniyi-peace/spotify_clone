from bs4 import BeautifulSoup
import requests

url = 'https://open.spotify.com'



html_content = requests.get(url)

soup = BeautifulSoup(html_content.content, 'html.parser').body
x = soup.find_all('div', class_='Box__BoxComponent-sc-y4nds-0')

artists_data = []
albums_data = []

try:
    

    for i in range(len(x)):

        # Scrape popular artist data

        if "artist" in x[i]["aria-labelledby"] and len(artists_data)<=9:
            artist_image_url=  x[i].find("img")["src"]
            artist_name = x[i].find("a").string
            artist_id = x[i].find("a")["href"].split('/')[-1]

            artists_data.append({
                'artist_name': artist_name,
                'artist_id': artist_id,
                'artist_image_url': artist_image_url
            })

        # Scrape popular album data

        elif "album" in x[i]["aria-labelledby"] and len(albums_data)<=9:
            album_image_url =  x[i].find("img")["src"]
            album_name = x[i].find("a").string
            anchor_tag_list = x[i].find_all("a")
            album_id = x[i].find("a")["href"].split('/')[-1]

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


except Exception as e:
    print(f"Error scraping spotify data: {e}")


# Output the scraped data
print("Artists Data:")
for artist in artists_data:
    print(f"Name: {artist['artist_name']}, ID: {artist['artist_id']}, Image URL: {artist['artist_image_url']}")

print("\nAlbums Data:")
for album in albums_data:
    print(f"Name: {album['album_name']}, Image URL: {album['album_image_url']}, Artist{album['album_artist']}. {'album_id'}")


