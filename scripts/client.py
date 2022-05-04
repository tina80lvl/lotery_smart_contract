import os
import json
from web3 import Web3

w3 = Web3(
    Web3.HTTPProvider(
        'https://rinkeby.infura.io/v3/13b0500f54974170a60327b443e4e063'
    )
)
chain_id = 4
owner_address = '0x829ec9b4c6048BFdcC11882339279146B7d78872'
owner_private = os.getenv('PRIVATE_KEY_0')
nonce = w3.eth.getTransactionCount(owner_address)

abi = json.load(open('build/contracts/Lotery.json'))['abi']
contract_address = '0x0120a7c1383D5F3e3F29287b8dAba7Edd7360fA9'


def get_participants_from_file(path):
    ''' JSON structure:
    [
        {
            "address": "0x3...fk", // wallet address
            "private": "PRIVATE_KEY_1", // name of the env var with private key
            "value": 0.02 // value to send to enter the lotery in ether
        },
        ...
    ]
    '''
    with open(path) as file:
        data = json.load(file)
        return data


def enter_participant(lotery, partic):
    print('Entering participant: ', partic['address'])

    greeting_transaction = lotery.functions.enter().buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": partic['address'],
            "value": Web3.toWei(partic['value'], 'ether'),
            "nonce": nonce + 1,
        }
    )
    
    signed_greeting_txn = w3.eth.account.sign_transaction(
        greeting_transaction, private_key=os.getenv(partic['private'])
    )
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    print("Done!")


def pick_winner_v1(lotery):
    greeting_transaction = lotery.functions.pickRandomWinner().buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": owner_address,
            # "nonce": nonce + 2,
        }
    )
    signed_greeting_txn = w3.eth.account.sign_transaction(
        greeting_transaction, private_key=os.getenv(owner_private)
    )
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    print('Prize fund is sent to the winner`s address!')


def pick_winner_v2(lotery):
    winner = lotery.functions.pickRandomWinner().call({'from': owner_address})
    print(f'The winner is: {winner}')


def interact(participants_pass):
    lotery = w3.eth.contract(address=contract_address, abi=abi)
    # just to check that we're connected
    print(f'Initial Lotery Balance: {lotery.functions.getBalance().call()}')

    participants_list = get_participants_from_file(participants_pass)

    for participant in participants_list:
        enter_participant(lotery, participant)
        print(f'Current Lotery Balance: {lotery.functions.getBalance().call()}')
    
    # # to make a screenshot
    # os.sleep(300000)

    # pick_winner_v2(lotery)
    # pick_winner_v1(lotery)



if __name__ == '__main__':
    interact('data/addresses.json')
    # get_participants_from_file('data/addresses.json')
