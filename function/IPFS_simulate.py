import uuid



def upload(data):
    CID = uuid.uuid4() # use uuid to simulate CID

    with open(f'./IPFS/{CID}.txt','w') as f:
        f.write(str(data))
    return CID
        
def download(CID):
    with open(f'./IPFS/{CID}.txt', 'r') as f:
        data = f.read()
    return data

