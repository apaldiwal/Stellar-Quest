"""
Quest Description:
Store some arbitrary data in your Stellar account. Stellar allows you to
store arbitrary data in the form of key:value pairs. In this challenge, you're
tasked with adding a key of 'Hello' and a value of 'World' as a data attribute
on your account. Note this challenge is case sensitive, so ensure you've got
your key and value properly capitalized before checking your answer.
"""

# 1. Import Libraries
print("Importing Libraries...")

import requests
from stellar_sdk import Server, Keypair, TransactionBuilder, Network

# 2. Load Stellar Quest Keypair
print("Loading Stellar Quest Keypair...")

QUEST_KEYPAIR = Keypair.from_secret("Enter Your Stellar Quest Secret Key")
QUEST_PK = QUEST_KEYPAIR.public_key
QUEST_SK = QUEST_KEYPAIR.secret

# 3. Store arbitrary data in Stellar Quest Account
print("Building Transaction...")

transaction = (
    TransactionBuilder (
        source_account = server.load_account(account_id = QUEST_PK),
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee = 100
    )
    .append_manage_data_op (
        data_name = "Hello",
        data_value = "World"
    )
    .set_timeout(30)
    .build()
)

print("Signing Transaction...")
transaction.sign(QUEST_SK)
response = server.submit_transaction(transaction)

print(f"This is the Final Response: {response}")
