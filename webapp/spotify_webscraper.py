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


def get_artist_details(artist_id):
    url = "https://spotify-scraper.p.rapidapi.com/v1/artist/overview"

    querystring = {"artistId":artist_id}

    headers = {
        "x-rapidapi-key": "cefcd605efmshfe83982a384c1cap10e73ajsnbf39a673f5df",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)


    if response.status_code == 200:
        response_data = response.json()

        name = response_data.get("name")
        biography = response_data.get("biography")
        monthly_listeners = response_data["stats"].get("monthlyListeners")
        header_image_url = response_data["visuals"]["header"][0].get("url")
        gallery_image_url = response_data["visuals"]["gallery"][1][0].get("url")
        albums = []
        tracks = []

        discography = response_data.get("discography")
        
        for items in discography.get("popularReleasesAlbums"):
            album_name = items.get("name")
            album_id = items.get("id")
            album_cover = items["cover"][1].get("url")

            albums.append({"album_name":album_name, "album_id":album_id, "album_cover":album_cover})

        for items in discography.get("topTracks"):
            track_name = items.get("name")
            track_id = items.get("id")
            track_duration = items.get("durationText")
            track_play_count = items.get("playCount")
            track_image_url = items["album"]["cover"][1].get("url")

            tracks.append({"track_name":track_name, "track_id":track_id, "track_duration":track_duration,
                           "track_play_count":track_play_count, "track_image_url":track_image_url})
            
        return {"name":name, "biography":biography, "monthly_listeners":monthly_listeners,
                "header_image_url":header_image_url, "gallery_image_url":gallery_image_url,
                "albums":albums, "tracks":tracks}
    
    else:
        print("Error get artist data")


def get_album_details(album_id):
    url = "https://spotify23.p.rapidapi.com/albums/"

    querystring = {"ids":album_id}

    headers = {
        "x-rapidapi-key": "cefcd605efmshfe83982a384c1cap10e73ajsnbf39a673f5df",
        "x-rapidapi-host": "spotify23.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        response_data = response.json()

        name = response_data["albums"][0].get("name")
        album_cover = response_data["albums"][0]["images"][1].get("url")
        artist = response_data["albums"][0]["artists"][0].get("name")
        artist_id = response_data["albums"][0]["artists"][0].get("id")
        total_tracks = response_data["albums"][0].get("total_tracks")
        release_date = response_data["albums"][0].get("release_date")
        track_list = []

        tracks = response_data["albums"][0]["tracks"].get("items")
        
        for items in tracks:
            track_id = items.get("id")
            track_name = items.get("name")
            track_number = items.get("track_number")
            track_duration = items.get("duration_ms")
            track_artist = items["artists"][0].get("name")

            if  len(items["artists"])>1:
                feat = "  feat. "

                for item in items["artists"]:
                    if item == items["artists"][0]:
                        pass
                    else:
                        feat += item.get("name")

                track_artist += feat

            track_list.append({"track_id":track_id, "track_name":track_name, "track_number":track_number,
                               "track_duration":track_duration, "track_artist":track_artist})
            
        return {"name":name, "album_cover":album_cover, "artist":artist,
                "artist_id":artist_id, "total_tracks":total_tracks, "release_date":release_date,
                "track_list":track_list}
    
    else:
        print("Error getting album data")