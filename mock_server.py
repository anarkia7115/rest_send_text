import flask
from flask import Flask, request
import json

app = flask.Flask(__name__)

@app.route("/annotate/text", methods=['POST'])
def annotate_mock():
    data_from_network = request.get_json()
    return json.dumps(data_from_network)