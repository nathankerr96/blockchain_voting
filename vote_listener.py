import time

def add_to_queue(vote):
    global vote_queue
    vote_queue.put(vote)

def start_listening():

    #get vote from network

    while True:
        vote = "test"

        add_to_queue(vote)

        time.sleep(0.5)


def begin(vq):
    global vote_queue
    vote_queue = vq


    start_listening()
