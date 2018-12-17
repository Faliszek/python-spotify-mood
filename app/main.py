import os
import urllib

from flask import Flask, send_file, jsonify, redirect, request
from flask_cors import CORS


from .conifg import Config

from api import TracksEndpoint
from api import PlaylistEndpoint
from app.utils import Utils

app = Flask(__name__)
CORS(app, resources=r'/api/*')


@app.route("/login")
def login():
    params = {
        "response_type": "token",
        "client_id": Config.CLIENT_ID,
        "scope": Config.SPOTIFY_SCOPE,
        "redirect_uri": Config.REDIRECT_URI
    }

    return redirect(Config.SPOTIFY_AUTH + '?' + urllib.parse.urlencode(params))


@app.route("/api/tracks")
def tracks():
    return TracksEndpoint.getAll()


@app.route("/api/playlist/<playlistId>", methods=['PUT'])
def updatePlaylist(playlistId):
    if request.method == 'PUT':
        return PlaylistEndpoint.update(playlistId)


@app.route("/api/playlist", methods=['POST', 'GET'])
def playlist():
    if request.method == 'GET':
        return PlaylistEndpoint.getAll()

    if request.method == 'POST':
        print('post to playlist')
        return PlaylistEndpoint.create()


# @app.route("/artists")
# def tracks():
#     return ArtistEndpoint.getAll()


@app.route("/")
def main():
    index_path = os.path.join(app.static_folder, 'index.html')
    return send_file(index_path)


# Everything not declared before (not a Flask route / API endpoint)...
@app.route('/<path:path>')
def route_frontend(path):
    # ...could be a static file needed by the front end that
    # doesn't use the `static` path (like in `<script src="bundle.js">`)
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    # ...or should be handled by the SPA's "router" in front end
    else:
        index_path = os.path.join(app.static_folder, 'index.html')
        return send_file(index_path)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=8080)
