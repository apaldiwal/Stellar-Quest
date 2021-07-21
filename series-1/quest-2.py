"""
Quest Description:
Make a payment from your Stellar account. In this challenge, your task is
to make a 10 XLM payment from the Stellar account you funded in challenge 1.
Use the payment operation to send the XLM payment to any other testnet account.
"""

# 1. Import Libraries
print("Importing Libraries...")

import requests
from stellar_sdk import Server, Keypair, TransactionBuilder, Network

# 2. Load Stellar Quest Keypair
print("Loading Stellar Quest Keypair...")

server = Server("https://horizon-testnet.stellar.org")
QUEST_KEYPAIR = Keypair.from_secret("Enter Your Stellar Quest Secret Key")
QUEST_PK = QUEST_KEYPAIR.public_key
QUEST_SK = QUEST_KEYPAIR.secret

# 3. Generate a Random Keypair
print("Generating Random Keypair...")

RANDOM_KEYPAIR = Keypair.random()
RANDOM_PK = RANDOM_KEYPAIR.public_key
RANDOM_SK = RANDOM_KEYPAIR.secret

# 4. Fund the Random Account via FriendBot
print("Funding Random Account...")

FRIENDBOT_URL = "https://friendbot.stellar.org"
response = requests.get(FRIENDBOT_URL, params={'addr': RANDOM_PK})
print(f"FriendBot responded with {response}")

# 5. Make a Payment from Stellar Quest Account to Random Account
print("Building Transaction...")

transaction = (
    TransactionBuilder (
        source_account = server.load_account(account_id = QUEST_PK),
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee = 100
    )
    .append_payment_op (
        destination = RANDOM_PK,
        amount = "10",
        asset_code="XLM"
    )
    .set_timeout(30)
    .build()
)

print("Signing Transaction...")
transaction.sign(QUEST_SK)
response = server.submit_transaction(transaction)

print(f"This is the Final Response: {response}")
