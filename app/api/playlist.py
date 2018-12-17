import sys
import urllib
import json
from flask import jsonify, request

from app.conifg import Config

from .middleware import Request
from model.playlist import PlaylistModel

from api.artist import ArtistEndpoint


class PlaylistEndpoint:

    def parseParams():
        params = {
            "offset": "1",
            "limit": "50"
        }

        return urllib.parse.urlencode(params)

    def getUserId():
        res = json.loads(Request.Get(
            Config.SPOTIFY_URI + '/me/'))

        if res['id']:
            return res['id']
        else:
            return Request.handleError()

    def getAll():
        parsedParams = PlaylistEndpoint.parseParams()

        print(parsedParams)
        res = json.loads(Request.Get(
            Config.SPOTIFY_URI + '/me/playlists?' + parsedParams))
        print(res)
        if not res['items']:
            return Request.handleError()

        playlists = list(map(PlaylistModel.mapPlaylist, res['items']))

        return jsonify({
            "playlists": playlists,
        })

    def create():
        data = request.get_json()
        userId = PlaylistEndpoint.getUserId()

        if data['name']:
            name = data['name']

            res = Request.Post(Config.SPOTIFY_URI +
                               '/users/'+userId+'/playlists', {"name": name})
            resData = json.loads(res)

            return jsonify({
                "id": resData["id"]
            })
        else:
            return jsonify({
                "error": "No name provided"
            })

    def update(playlistId):
        data = request.get_json()

        if data["uris"]:
            res = Request.Put(Config.SPOTIFY_URI +
                              '/playlists/'+playlistId+'/tracks',
                              {"uris": data["uris"]})
            resData = json.loads(res)

            return jsonify({
                "id": resData["snapshot_id"]
            })

        else:
            return jsonify({
                "error": "No tracks prvoided"
            })
