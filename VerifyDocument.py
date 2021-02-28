import hashlib
# function that compare the smart contract
def get_hash(contracthash):
    #List that store the hash of the true smart contract 
    lstSmartContract = ["d8fc8839456e636d5cd3cb7e8642ce5a4d2b3a53bc02690d2b2ea0b0639c57eb", 
                        "3201213b4a5b08faed2176fe4d32a7aa08db2ded03dde26cc9a07318c54ca4e5"] 
    for x in range(len(lstSmartContract)):
        if contracthash == lstSmartContract[x]:
            #return the hash if it matches the right contract
            return lstSmartContract[x]
            break
        else:
            #return a space if nothing is found
            return " "
            
    
# Ask user to input the file name
file = input("Input your file name to check the hash:") 
BLOCK_SIZE = 65536 
#Generate hash of the tt file
file_hash = hashlib.sha256() 
with open(file, 'rb') as f: 
    fb = f.read(BLOCK_SIZE) 
    while len(fb) > 0: 
        file_hash.update(fb) 
        fb = f.read(BLOCK_SIZE) 

# Verify the smart contract by comparing the hash
if file_hash.hexdigest() == get_hash(file_hash.hexdigest()):
    #Consequence exists if return lstSmartContract[x] is run in def get_hash(contracthash):
    print("It is a valid smart contract")
else:
    #Consequence exists if return " " is run in def get_hash(contracthash):
    print("It is an invalid smart contract")



