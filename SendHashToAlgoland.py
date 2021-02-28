import ssl
import json
import base64
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk.future.transaction import PaymentTxn

ssl._create_default_https_context = ssl._create_unverified_context

# utility for waiting on a transaction confirmation
def wait_for_confirmation(client, transaction_id, timeout):
    """
    Wait until the transaction is confirmed or rejected, or until 'timeout'
    number of rounds have passed.
    Args:
        transaction_id (str): the transaction to wait for
        timeout (int): maximum number of rounds to wait    
    Returns:
        dict: pending transaction information, or throws an error if the transaction
            is not confirmed or rejected in the next timeout rounds
    """
    start_round = client.status()["last-round"] + 1;
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return 
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:  
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)                   
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))

def send_note():
   algod_address = "https://testnet-algorand.api.purestake.io/ps2"
   algod_token = "WgL4G2ZZf22GsqUIKHvCY9BSJyXQzZS8aTIpnMnp"
   headers = {
      "X-API-Key": algod_token,
   }

   algod_client = algod.AlgodClient(algod_token, algod_address, headers)

   # In addition to setting up the client and transaction
   # See GitHub for wait_for_confirmation() definition

   # get suggested parameters from Algod
   params = algod_client.suggested_params()

   gen = params.gen
   gh = params.gh
   first_valid_round = params.first
   last_valid_round = params.last
   fee = params.min_fee
   send_amount = 1


   passphrase = "giraffe push drop glove cave cancel around roof talk example surprise atom foil outside anger right pistol stadium agent scheme patient script enrich able green"
   private_key = mnemonic.to_private_key(passphrase)
   my_address = mnemonic.to_public_key(passphrase)
   print("My address: {}".format(my_address))
   params = algod_client.suggested_params()
   print(params)
   # comment out the next two (2) lines to use suggested fees
   params.flat_fee = True
   params.fee = 1000
   note = 'd8fc8839456e636d5cd3cb7e8642ce5a4d2b3a53bc02690d2b2ea0b0639c57eb'.encode() #content should be the hash
   receiver = "GOXL7P62EJNZF6B2ISN3EHT3NX6NWD4HQ77ER7WJRQRO5YGHNGT3RGL5LA"

   unsigned_txn = PaymentTxn(my_address, params, receiver, 1000000, None, note)

   # sign transaction
   signed_txn = unsigned_txn.sign(private_key)
    # send transaction
   txid = algod_client.send_transaction(signed_txn)
   print("Send transaction with txID: {}".format(txid))

    # wait for confirmation
   try:
       confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
   except Exception as err:
       print(err)
       return
    
   print("txID: {}".format(txid), " confirmed in round: {}".format(
       confirmed_txn.get("confirmed-round", 0)))       
   print("Transaction information: {}".format(
       json.dumps(confirmed_txn, indent=2)))
   print("Decoded note: {}".format(base64.b64decode(
       confirmed_txn["txn"]["txn"]["note"]).decode()))
   
send_note()
