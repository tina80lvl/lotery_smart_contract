from brownie import Lotery, accounts
from web3 import Web3


def test_updating_storage():
    # Arrange - deploy SimpleStorage smart contract.
    owner_account = accounts[0]
    instance = Lotery.deploy({'from': owner_account})

    participant1 = accounts[1]
    participant2 = accounts[2]
    participant3 = accounts[3]

    val = Web3.toWei(3, 'ether')
    instance.enter({'from': participant1, 'value': val})

    balance = instance.getBalance()

    assert balance == val
    