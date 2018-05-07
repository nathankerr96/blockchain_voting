from multiprocessing import Process, Queue, Manager

import blockchain
import vote_listener
import flask_listener


def main():
    manager = Manager()
    vote_queue = Queue()
    incoming_vote_queue = Queue()


    blockchain_process = Process(target=blockchain.begin, args=(vote_queue,))
    listener_process = Process(target=vote_listener.begin, args=(vote_queue, incoming_vote_queue))
    flask_process = Process(target=flask_listener.begin, args=(incoming_vote_queue,))

    blockchain_process.start()
    listener_process.start()
    flask_process.start()

    blockchain_process.join()


if __name__ == "__main__":
    main()
