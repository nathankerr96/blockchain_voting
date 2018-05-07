from urllib.parse import unquote
import json

from flask import Flask, request
import time

def begin(incoming_queue):
    print("SETTING UP:")


    app = Flask(__name__)

    @app.route("/")
    def main():
        args = request.args
        vote = args['vote']

        vote = unquote(vote)

        vote = json.loads(vote)

        incoming_queue.put(vote)
        
        print("KEY:", vote['public_key'])
        print("VOTE:", vote['ballot']['clinton'])
        print("SIGNATURE:", vote['signature'])

        return "Success!"

    app.run(debug=True, host='0.0.0.0')


