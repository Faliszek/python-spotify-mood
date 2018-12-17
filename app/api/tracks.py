import sys
import urllib
import json
from flask import jsonify, request

from app.conifg import Config
from app.utils import Utils

from .middleware import Request
from model.tracks import TracksModel

from api.artist import ArtistEndpoint


class TracksEndpoint:

    def parseParams(request):
        offset = int(request.args.get("offset"))
        limit = int(request.args.get("limit"))

        params = {
            "offset": offset,
            "limit": limit
        }

        return urllib.parse.urlencode(params)

    def countPercent(response, request):
        total = response['total']
        offset = response['offset']
        limit = int(request.args.get("limit"))

        actualOffset = offset + limit
        leftPercent = (total - actualOffset) / total
        return 1 - leftPercent if actualOffset < total else 1

    def getAll():
        parsedParams = TracksEndpoint.parseParams(request)

        res = json.loads(Request.Get(
            Config.SPOTIFY_URI + '/me/tracks?' + parsedParams))

        if not res['items']:
            return Request.handleError()

        tracks = list(map(TracksModel.mapTracks, res['items']))

        artists = ArtistEndpoint.fetchAll(tracks)

        tracksWithArtists = list(map(
            lambda t: TracksModel.assignArtistToTracks(t, artists),
            tracks))

        tracksWithGenres = list(map(
            lambda t: TracksModel.assignGenresToTracks(t, artists),
            tracksWithArtists))

        percent = TracksEndpoint.countPercent(res, request)
        total = res['total']

        return jsonify({
            "percent": int(percent * 100),
            "total": total,
            "tracks": tracksWithGenres,
        })
