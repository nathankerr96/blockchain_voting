import hashlib
import blockchain
import json

def verify_vote(vote):
    '''
        check that the ballot is valid and check that the 
        signature is valid
    '''
    return verify_ballot(vote["ballot"]) and verify_sign(vote)

def verify_ballot(user, real):
    '''
        makes sure that the ballot is in the correct form
    '''
    #user = json.loads(vote)
    #real = json.loads(real_ballot)

    # iterate through the user ballot and verify it works
    for field1, field2 in zip(user, real):
        if user[field1] != real[field2]:
            return False

        for candidate1, canidate2 in zip(user[field1], real[field2]):
            if user[field1][candidate1] != user[field2][candidate2]:
                return False

    return True

def verify_sign(vote):
    '''
        makes sure that the signature on the ballot is valid
    '''
    ballot_hash = hashlib.sha256(vote["ballot"]).hexdigest()
    int_ballot_hash = int(ballot_hash, 16)
    mod = vote["public_key"]["public_key_n"] 
    exp = public["public_key"]["public_key_e"]

    mod = base64.b64decode(mod)
    mod = mod.encode('hex')
    mod = int(mod, 16)

    exp = base64.b64decode(exp)
    exp = mod.encode('hex')
    exp = int(exp, 16)

    unsigned_ballot = base64.b64decode(vote["signature"])
    unsigned_ballot = unsigned_ballot.encode('hex')
    unsigned_ballot = int(unsigned_ballot, 16)

    decrypt_signature = pow(unsigned_ballot, exp, mod)

    return (decrypt_signature == int_ballot_hash)

if __name__ == "__main__":
    pass
