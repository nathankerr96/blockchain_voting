from multiprocessing import Process, Queue, Manager, Array

import blockchain
import vote_listener
import flask_listener


def control_main():
    #manager = Manager()
    vote_queue = Queue()
    incoming_vote_queue = Queue()
    blocks_queue = Queue()


    print("START")
    blockchain_process = Process(target=blockchain.begin_blockchain, args=(vote_queue, blocks_queue))
    print("START2")
    #listener_process = Process(target=vote_listener.begin_listener, args=(vote_queue, incoming_vote_queue))
    print("START3")
    flask_process = Process(target=flask_listener.begin_flask, args=(vote_queue, blocks_queue))
    print("START4")

    blockchain_process.start()
    #listener_process.start()
    flask_process.start()

    blockchain_process.join()


if __name__ == "__main__":
    control_main()
