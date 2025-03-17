from bs4 import BeautifulSoup
import requests
import yt_dlp
from os import getenv

api_key = getenv("api_key")



def spotify_webscrapper():

    try:
        html_content = requests.get('https://open.spotify.com')

        soup = BeautifulSoup(html_content.content, 'html.parser').body
        divs = soup.find_all('div', class_='Box__BoxComponent-sc-y4nds-0')

        artists_data = []
        albums_data = []
        

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
    

    except requests.exceptions.RequestException as e:
        print(f"Error fetching artist data: {e}")
        return None  

    except (KeyError, TypeError, IndexError) as e:  # Handle JSON parsing errors or missing data
        print(f"Error parsing artist data: {e}")
        return None  

    except Exception as e: # Catch any other unexpected error.
        print(f"Error scraping spotify data: {e}")
        return None  



def get_artist_details(artist_id):
    url = "https://spotify23.p.rapidapi.com/artist_overview/"

    querystring = {"id":artist_id}

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "spotify23.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)


        if response.status_code == 200:
            response_data = response.json()

            name = response_data["data"]["artist"]["profile"].get("name")
            id = response_data["data"]["artist"].get("id")
            biography = response_data["data"]["artist"]["profile"]["biography"].get("text")
            monthly_listeners = response_data["data"]["artist"]["stats"].get("monthlyListeners")

            if  response_data["data"]["artist"]["visuals"]["headerImage"]:
                header_image_url = response_data["data"]["artist"]["visuals"]["headerImage"]["sources"][0].get("url")
            else:
                header_image_url = None

            if  response_data["data"]["artist"]["visuals"]["avatarImage"]:
                avatar_image_url = response_data["data"]["artist"]["visuals"]["avatarImage"]["sources"][1].get("url")
            else:
                avatar_image_url = None

            if  response_data["data"]["artist"]["visuals"]["gallery"]["items"]:
                gallery_image_url = response_data["data"]["artist"]["visuals"]["gallery"]["items"][0]["sources"][0].get("url")
            else:
                gallery_image_url = None
            albums = []
            tracks = []

            discography = response_data["data"]["artist"].get("discography")
            
            for items in discography["albums"].get("items"):
                album_name = items["releases"]["items"][0].get("name")
                album_id = items["releases"]["items"][0].get("id")
                album_cover = items["releases"]["items"][0]["coverArt"]["sources"][0].get("url")
                release_year = items["releases"]["items"][0]["date"].get("year")

                albums.append({"album_name":album_name, "album_id":album_id, "album_cover":album_cover,
                            "release_year":release_year})

            for items in discography["topTracks"].get("items"):
                track_name = items["track"].get("name")
                track_id = items["track"].get("id")
                track_duration = items["track"]["duration"].get("totalMilliseconds")
                track_play_count = items["track"].get("playcount")
                track_image_url = items["track"]["album"]["coverArt"]["sources"][1].get("url")

                tracks.append({"track_name":track_name, "track_id":track_id, "track_duration":track_duration,
                            "track_play_count":track_play_count, "track_image_url":track_image_url})
                
            return {"id":id, "name":name, "biography":biography, "monthly_listeners":monthly_listeners,
                    "header_image_url":header_image_url, "gallery_image_url":gallery_image_url,
                    "albums":albums, "tracks":tracks, "avatar_image_url":avatar_image_url}
        
        else:
            print("Error getting artist data")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching artist data: {e}")
        return None  # Return None to indicate an error

    except (KeyError, TypeError, IndexError) as e:  # Handle JSON parsing errors or missing data
        print(f"Error parsing artist data: {e}")
        return None  # Return None to indicate an error

    except Exception as e: # Catch any other unexpected error.
        print(f"An unexpected error occurred: {e}")
        return None  # Return None to indicate an error




def get_album_details(album_id):
    url = "https://spotify23.p.rapidapi.com/albums/"

    querystring = {"ids":album_id}

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "spotify23.p.rapidapi.com"
    }

    try:
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
                track_artists = []

                for artist in items["artists"]:
                    id = artist.get("id")
                    artist = artist.get("name")
                    track_artists.append({"name":artist, "id":id})

                # if  len(items["artists"])>1:
                #     feat = "  feat. "

                #     for item in items["artists"]:
                #         if item == items["artists"][0]:
                #             pass
                #         else:
                #             feat += item.get("name")

                #     track_artist += feat

                track_list.append({"track_id":track_id, "track_name":track_name, "track_number":track_number,
                                "track_duration":track_duration, "track_artist":track_artists})
                
            return {"name":name, "album_cover":album_cover, "artist":artist,
                    "artist_id":artist_id, "total_tracks":total_tracks, "release_date":release_date,
                    "track_list":track_list}
        
        else:
            print("Error getting album data ", response.status_code)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching artist data: {e}")
        return None  # Return None to indicate an error

    except (KeyError, TypeError, IndexError) as e:  # Handle JSON parsing errors or missing data
        print(f"Error parsing artist data: {e}")
        return None  # Return None to indicate an error

    except Exception as e: # Catch any other unexpected error.
        print(f"An unexpected error occurred: {e}")
        return None  # Return None to indicate an error




def get_search(query):

    url = "https://spotify23.p.rapidapi.com/search/"

    querystring = {"q":query,"type":"multi","offset":"0","limit":"10","numberOfTopResults":"7"}

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "spotify23.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            response_data = response.json()
            albums = []
            artists = []
            tracks = []
            top_result = {}

            for album in response_data["albums"].get("items"):
                id = album["data"].get("uri").split(":")[-1]
                name = album["data"].get("name")
                release_date = album["data"]["date"].get("year")
                cover = album["data"]["coverArt"]["sources"][0].get("url")
                artist_id = album["data"]["artists"]["items"][0].get("uri").split(":")[-1]
                artist = album["data"]["artists"]["items"][0]["profile"].get("name")

                albums.append({"id":id, "name":name, "release_date":release_date, "cover":cover,
                            "artist_id":artist_id, "artist":artist})
                
            for artist in response_data["artists"].get("items"):
                id = artist["data"].get("uri").split(":")[-1]
                name = artist["data"]["profile"].get("name")
                if artist["data"]["visuals"]["avatarImage"]:
                    image_url = artist["data"]["visuals"]["avatarImage"]["sources"][0].get("url")
                else:
                    image_url = None
                artists.append({"id":id, "name":name, "image_url":image_url})

            for track in response_data["tracks"].get("items"):
                if track["data"]:
                    id = track["data"].get("id")
                    name = track["data"].get("name")
                    album = track["data"]["albumOfTrack"].get("name")
                    album_id = track["data"]["albumOfTrack"].get("id")
                    album_cover = track["data"]["albumOfTrack"]["coverArt"]["sources"][0].get("url")
                    track_artists = []
                    duration = track["data"]["duration"].get("totalMilliseconds")

                    for artist in track["data"]["artists"]["items"]:
                        artist_name = artist["profile"].get("name")
                        artist_id = artist.get("uri").split(":")[-1]
                        track_artists.append({"id":artist_id, "name":artist_name})

                    tracks.append({"id":id, "name":name, "album":album, "album_id":album_id, "album_cover":album_cover,
                                "artists":track_artists, "duration":duration})

            for top in response_data["topResults"].get("items"):
                if "artist" in top["data"].get("uri") and query.lower() in top["data"]["profile"].get("name").lower():
                    top_result['type'] = "Artist"
                    top_result['id'] = top["data"].get("uri").split(":")[-1]
                    top_result['name'] = top["data"]["profile"].get("name")
                    if top["data"]["visuals"]["avatarImage"]:
                        top_result['image_url']  = top["data"]["visuals"]["avatarImage"]["sources"][0].get("url")
                    else:
                        top_result['image_url']  = None
                        break

                elif "album" in top["data"].get("uri") and query.lower() in top["data"].get("name").lower():
                    top_result['type'] = "Album"
                    top_result['id'] = top["data"].get("uri").split(":")[-1]
                    top_result['name'] = top["data"].get("name")
                    top_result['release_date'] = top["data"]["date"].get("year")
                    top_result['image_url'] = top["data"]["coverArt"]["sources"][0].get("url")
                    top_result['artist_id'] = top["data"]["artists"]["items"][0].get("uri").split(":")[-1]
                    top_result['artist'] = top["data"]["artists"]["items"][0]["profile"].get("name")
                    break


                
            
            if top_result == {}:
                for top in response_data["topResults"].get("items"):
                    if "artist" in top["data"].get("uri"):
                        top_result['type'] = "Artist"
                        top_result['id'] = top["data"].get("uri").split(":")[-1]
                        top_result['name'] = top["data"]["profile"].get("name")

                        if top["data"]["visuals"]["avatarImage"]:
                            top_result['image_url']  = top["data"]["visuals"]["avatarImage"]["sources"][0].get("url")
                        else:
                            top_result['image_url']  = None
                            break
            
                    
        
            return {"albums":albums, "artists":artists, "tracks":tracks, "top_result":top_result}
        
        else:
            print("error getting search data")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching artist data: {e}")
        return None  # Return None to indicate an error

    except (KeyError, TypeError, IndexError) as e:  # Handle JSON parsing errors or missing data
        print(f"Error parsing artist data: {e}")
        return None  # Return None to indicate an error

    except Exception as e: # Catch any other unexpected error.
        print(f"An unexpected error occurred: {e}")
        return None  # Return None to indicate an error




def get_track_audio_url(query):
    url = "https://spotify-scraper.p.rapidapi.com/v1/track/download/soundcloud"

    querystring = {"track":"Photograph Ed Sheeran","quality":"sq"}

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response_data.status_code == 200:
            response_data = response.json()
            audio_url = response_data["soundcloudTrack"]["audio"][0].get("url")
            return audio_url

        else:
            print("Error getting song data")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching artist data: {e}")
        return None  

    except (KeyError, TypeError, IndexError) as e:  # Handle JSON parsing errors or missing data
        print(f"Error parsing artist data: {e}")
        return None  

    except Exception as e: # Catch any other unexpected error.
        print(f"An unexpected error occurred: {e}")
        return None  

    

def search_song(id):

    url = "https://spotify23.p.rapidapi.com/tracks/"

    querystring = {"ids":id}

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "spotify23.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            response_data = response.json()["tracks"][0]
            cover_image = response_data["album"]["images"][0].get("url")
            name = response_data.get("name")
            duration = response_data.get("duration_ms")
            artists = []
            artist_name_only = ""

            for artist in response_data["artists"]:
                artist_name = artist.get("name")
                id = artist.get("id")
                artists.append({"id":id, "artist_name":artist_name})
                artist_name_only  += artist_name+" "
                

            # # Set up yt-dlp options to search for the song
            # ydl_opts = {
            #     'format': 'bestaudio/best',  # Best audio quality
            #     'quiet': True,  # Suppress output except for essential
            #     'extractaudio': True,  # Only extract audio
            #     'noplaylist': True,  # Don't download playlists
            #     'simulate': True,  # Don't download, just simulate and get metadata
            #     'force_generic_extractor': True,  # Use the generic extractor
            #     'cookies_from_browser': ('chrome', "firefox"),
            #     'cookiefile': 'cookies.txt',  # Path to your exported cookies
            # }

            # # Construct the search query
            # query = f"{name} {artist_name_only}"

            # # Use yt-dlp to search and get the video information
            # with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            #     info = ydl.extract_info(f"ytsearch:{query}", download=False)
                
            #     if 'entries' in info:
            #         # Grab the first video result
            #         video = info['entries'][0]
            #         video_url = video['url']  # This is the video URL
            #         return {"name":name, "cover_image":cover_image, 
            #                 "artists":artists, "duration":duration, "audio_url":video_url}

            # url = "https://spotify-scraper.p.rapidapi.com/v1/track/download/soundcloud"

            # querystring = {"track":f"{name} {artist_name_only}","quality":"sq"}

            # headers = {
            #     "x-rapidapi-key": api_key,
            #     "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
            # }
            
            # response = requests.get(url, headers=headers, params=querystring)

            # if response.status_code == 200:
            #     response_data = response.json()
            #     audio_url = response_data["soundcloudTrack"]["audio"][0].get("url")
            #     return {"name":name, "cover_image":cover_image, 
            #                 "artists":artists, "duration":duration, "audio_url":audio_url}
            
            # else:
            #     return {"name":name, "cover_image":cover_image, 
            #                 "artists":artists, "duration":duration, "audio_url":"https://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/Sevish_-__nbsp_.mp3"}
            ydl_opts = {
                'format': 'bestaudio/best',  # Best audio quality
                'quiet': True,  # Suppress output except for essential
                'extractaudio': True,  # Only extract audio
                'noplaylist': True,  # Don't download playlists
                'simulate': True,  # Don't download, just simulate and get metadata
                'force_generic_extractor': True,  # Use the generic extractor
                'cookies_from_browser': ('chrome', "firefox"),
                'cookiefile': 'cookies.txt',  # Path to your exported cookies
            }

            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info("https://www.youtube.com/watch?v=d_HlPboLRL8", download=False)
                video_url = info['url']  # This is the video URL
                return {"name":name, "cover_image":cover_image, 
                            "artists":artists, "duration":duration, "audio_url":video_url}

        else:
            print("Error getting song data")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching artist data: {e}")
        return None  

    except (KeyError, TypeError, IndexError) as e:  # Handle JSON parsing errors or missing data
        print(f"Error parsing artist data: {e}")
        return None  

    except Exception as e: # Catch any other unexpected error.
        print(f"An unexpected error occurred: {e}")
        return None  

def test():
    # Set up yt-dlp options to search for the song
    ydl_opts = {
        'format': 'bestaudio/best',  # Best audio quality
        'quiet': True,  # Suppress output except for essential
        'extractaudio': True,  # Only extract audio
        'noplaylist': True,  # Don't download playlists
        'simulate': True,  # Don't download, just simulate and get metadata
        'force_generic_extractor': True,  # Use the generic extractor
        'cookies_from_browser': ('chrome', "firefox"),
        'cookiefile': 'cookies.txt',  # Path to your exported cookies
    }

    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info("https://www.youtube.com/watch?v=d_HlPboLRL8", download=False)
        video_url = info['url']  # This is the video URL
        print(video_url)


