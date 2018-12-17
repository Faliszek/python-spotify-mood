import requests
import json
import sys

from flask import request, jsonify, Response
from app.utils import Utils


class Request:
    def setHeaders():
        token = request.headers.get('Authorization')
        headers = {"Authorization": token}
        return headers

    def handleRequest(req):

        if req.status_code == 200 or req.status_code == 201:
            return json.dumps(req.json())
        else:
            return Request.handleError()

    def Get(url):
        headers = Request.setHeaders()
        req = requests.get(url, headers=headers)
        return Request.handleRequest(req)

    def Post(url, payload):
        headers = Request.setHeaders()
        req = requests.post(url, headers=headers, data=json.dumps(payload))
        return Request.handleRequest(req)

    def Put(url, payload):
        headers = Request.setHeaders()
        req = requests.put(url, headers=headers, data=json.dumps(payload))
        return Request.handleRequest(req)

    def handleError():
        return jsonify(
            Response("{'message': 'Something went wrong'}",
                     status=400,
                     mimetype='application/json').json())
