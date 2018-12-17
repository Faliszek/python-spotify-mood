
class ArtistModel:
    def mapArtist(a):
        return {
            "id": a['id'],
            "name": a['name'],
            "genres": a['genres'],
            "image": ArtistModel.getArtistSmallImage(a)
        }

    def getArtistSmallImage(artist):
        images = artist['images']
        for img in images:
            if img['width'] > 60 and img['width'] < 240:
                return img

    def getAllIds(artists):
        return list(map(lambda a: a['id'], artists))
