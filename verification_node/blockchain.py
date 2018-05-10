import hashlib
import secrets

from multiprocessing import Queue

#Length of the hash in bits
HASH_LENGTH = 256

class Block:

    #how many leading 0's are needed to accept a hash, adding 1 will double difficulty
    _INITIAL_DIFFICULTY = 18


    def __init__(self, prev_hash):

        #vars used in block hashing
        self._prev_hash = prev_hash
        self._votes = tuple()
        self._nonce = 0

        #pointer to next block, set when complete
        self.next_block = None

        #set initial difficulty for the block 
        self.set_difficulty(self._INITIAL_DIFFICULTY)


    def set_difficulty(self, difficulty):
        self._difficulty = difficulty


    def add_vote(self):
        pass


    def _get_test_string(self):
        """Creates the test string according to the set difficulty

        The test string will have `self._difficulty` leading 0's followed by 1's giving
            a total length of `HASH_LENGTH`.
        Because Python interprets the hash_string as a list of ints when iterated through,
            we construct the test string the same way (i.e. a list of ints that represent
            byte values)
        
        Returns:
            (list(int))- list of ints representing bytes which make up the test string
        """

        #mapping number of leading 0's to the integer corresponding to that byte
        difficulty_mapping = { 0 : 255, 1 : 127, 2 : 63, 3 : 31, 4 : 15, 5 : 7, 6 : 3, 7 : 1}

        test_string = list()
        difficulty_left = self._difficulty

        #if we need more than 8 leading bytes, append a 0 byte
        while difficulty_left >= 8:
            test_string.append(0)
            difficulty_left -= 8

        #assign last leading byte based on the remaning number of leading 0's needed 
        test_string.append(difficulty_mapping[difficulty_left])

        #fill out the rest of the bitstring with 1's (int 255)
        while len(test_string) < (HASH_LENGTH / 8):
            test_string.append(255)

        return test_string


    def _or(self, test_string, hash_string):
        """Function to take bitwise OR of the test and hash strings

        Expects strings to be lists of intergers representing bytes and returns
            the same

        Args:
            test_string (bytes): the string to test against
            hash_string (list(int)): the hash string to test

        Returns:
            (list(int)): the bitwise OR result list
        """

        result_string = list()

        #bitwise OR each corresponding entry in the two lists
        for t, h in zip(test_string, hash_string):
            result_string.append(t | h)

        return result_string


    def _accept_hash(self, hash_string):
        """Tests if the passed hash has enough leading 0's as defined by `self._difficulty`

        We test this by creating a "bitmask" with the target number of leading 0's,
            bitwise ORing it with the hash_string and seeing if the resulting string
            is the same as the target_string (which will happen only if the hash_string
            contains enough leading 0's)
        Because Python naturally interprets the hash_string as a sequecne of ints when iterating
            over it, we do the same for our target "bitmask"

        Args:
            hash_string (bytes): the hash_string to test

        Returns:
            (bool): True if the hash_string has enough leading 0's, False otherwise
        """
        test_string = self._get_test_string()

        result_string = self._or(test_string, hash_string)

        return result_string == test_string


    def mine(self):
        """Main method to mine the block

        Hashes the block, tests the hash, and increases the nonce until
            an acceptable hash is found
        Meanwhile, votes will continue being added to the tuple of votes

        Returns:
            (bytes): the hash_string of the final block
        """
        while True:
            hash_string = self.calc_hash()
            
            if self._accept_hash(hash_string):
                #print("success")
                print(self._nonce)
                print(self._votes)
                return hash_string

            self._add_votes()
            self._nonce += 1


    def _add_votes(self):
        new_votes = get_votes_in_queue()
        self._votes = self._votes + new_votes


    def calc_hash(self):
        if HASH_LENGTH == 256:
            h = hashlib.sha256()
        else:
            print("Unknown Hash Function!")
            exit(1)
        h.update(self._prev_hash)
        #TODO: should only add each vote once
        for vote in self._votes:
            h.update(vote.encode())
        h.update(self._nonce.to_bytes(self._nonce.bit_length(), byteorder='big'))

        hash_string = h.digest()

        return hash_string


    def verify(self, reported_hash):
        block_hash = self.calc_hash()
        
        return reported_hash == block_hash



class BlockChain:

    def __init__(self):
        self.base_block = self._create_base_block()
        self.current_block = self.base_block 


    def _create_base_block(self):
        return Block(secrets.token_bytes(HASH_LENGTH))

    def start(self):
        global blocks_queue
        block_count = 0

        while True:
            #mine block
            hash_string = self.current_block.mine()

            '''
            if self.current_block.verify(hash_string):
                print("Verified!")
            else:
                print("Not verified.")
            '''

            #block has been solved, create new block

            new_block = Block(hash_string)
            self.current_block.next_block = new_block
            
            #blocks_queue.put_nowait(self.current_block)
            blocks_queue.put_nowait(block_count)
            print("Put", block_count, "in queue")
            block_count += 1

            self.current_block = new_block


def get_votes_in_queue():
    global vote_queue
    vote_list = list()
    while not vote_queue.empty():
        vote = vote_queue.get_nowait()

        vote_list.append(vote)
    
    return tuple(vote_list)


def begin_blockchain(vq, bq):
    global vote_queue
    global blocks_queue
    vote_queue = vq
    blocks_queue = bq

    bchain = BlockChain()
    bchain.start()
    

'''
def main():
    global vote_queue
    vote_queue = Queue()

    blockchain = BlockChain()
    blockchain.start()

if __name__ == "__main__":
    main()
'''
