

def music(request):
    data = SongSession(request)
    return {"song":data.get_song()}


class SongSession(object):
    def __init__(self, request):
        self.session = request.session

        if not self.session.get("song"):
            self.song = self.session["song"] = {}
        
        self.song = self.session.get("song")


    def save_song(self, artists, name, cover_image, duration, audio_url):
        self.session["song"] = {"artists":artists, "name":name, "cover_image":cover_image, 
                                "duration":duration, "audio_url":audio_url}
        self.session.modified = True

    def get_song(self):
        return self.song
        
