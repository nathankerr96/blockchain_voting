from multiprocessing import Process, Queue, Manager

import blockchain
import vote_listener


def main()
    manager = Manager()
    vote_queue = Queue()


    blockchain_process = Process(target=blockchain.begin, args=(vote_queue,))
    listener_process = Process(target=vote_listener.begin, args=(vote_queue,))

    blockchain_process.start()
    listener_process.start()

    blockchain_process.join()


if __name__ == "__main__":
    main()
