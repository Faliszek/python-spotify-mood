class TracksModel:

    def getTrackBigImage(track):
        images = track['album']['images']
        for img in images:
            if img["width"] < 660 and img["width"] > 500:
                return img

    def mapAlbum(track):
        album = track["album"]
        return {
            "id": album['id'],
            "name": album['name'],
        }

    def mapTracks(t):

        return {
            "id": t['track']['id'],
            "name": t['track']['name'],
            "image": TracksModel.getTrackBigImage(t['track']),
            "album": TracksModel.mapAlbum(t['track']),
            "url": t['track']['href'],
            "duration_ms": t['track']['duration_ms'],
            "artist": t['track']['artists'][0],
            "uri": t['track']['uri']
        }

    def assignGenresToTracks(track, artists):
        newTrack = track
        for artist in artists:
            if artist['id'] == track['artist']['id']:
                newTrack['genres'] = artist['genres']
                return newTrack

    def assignArtistToTracks(track, artists):
        newTrack = track
        for a in artists:
            if a['id'] == track['artist']['id']:
                artist = {
                    "id": a['id'],
                    "name": a['name'],
                    "image": a['image']
                }
                newTrack['artist'] = artist

                return newTrack
