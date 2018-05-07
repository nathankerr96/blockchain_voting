import time

def add_to_queue(vote):
    global vote_queue
    vote_queue.put(vote)

def start_listening():
    global incoming_vote_queue

    #get vote from network

    while True:
        vote = incoming_vote_queue.get()

        add_to_queue(str(vote))

        time.sleep(0.5)


def begin(vq, ivq):
    global vote_queue
    global incoming_vote_queue

    vote_queue = vq
    incoming_vote_queue = ivq



    start_listening()
