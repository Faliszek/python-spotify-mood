import json

from .middleware import Request
from app.conifg import Config
from app.utils import Utils


from model.artist import ArtistModel


class ArtistEndpoint:

    def fetchAll(tracks):
        artistsDuplicated = list(map(lambda t: t['artist'], tracks))

        artists = Utils.removeDuplicateInList(artistsDuplicated)
        artistsIds = ArtistModel.getAllIds(artists)
        artistsIdsString = ",".join(artistsIds)

        artistsResponse = json.loads(Request.Get(
            Config.SPOTIFY_URI + '/artists?ids=' + artistsIdsString))
        return list(map(ArtistModel.mapArtist, artistsResponse['artists']))

    def getAll(tracks):
        return ArtistEndpoint.fetchAll(tracks)
