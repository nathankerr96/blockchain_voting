from urllib.parse import unquote
import json

from flask import Flask, request
import time

def begin_flask(incoming_queue, blocks_queue):
    print("SETTING UP:")


    app = Flask(__name__)

    @app.route("/")
    def accept_vote():
        print("HERE")
        args = request.args
        vote = args['vote']

        vote = unquote(vote)

        vote = json.loads(vote)

        incoming_queue.put(vote)
        
        print("KEY:", vote['public_key'])
        print("VOTE:", vote['ballot']['clinton'])
        print("SIGNATURE:", vote['signature'])

        return "Success!"


    known_blocks = []
    @app.route("/view_blockchain")
    def print_blockchain():
        '''
        while not blocks_queue.empty():
            block = blocks_queue.get_nowait()
            print("got block with nonce: ", block._nonce)
            known_blocks.append(block)
        '''
        while True:
            try:
                block = blocks_queue.get_nowait()
                #print("got block with nonce: ", block._nonce)
                known_blocks.append(block)
            except:
                break
            

        #nonces = [str(b._nonce) for b in known_blocks]
        nonces = [str(b) for b in known_blocks]

        return ', '.join(nonces)

    app.run(debug=True, host='0.0.0.0', use_reloader=False)


