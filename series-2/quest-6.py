"""
Quest Description:
Sponsor the absolute minimum balance for a new account. In this challenge your
task is to create a brand new 0 XLM balance account with the absolute minimum
balance sponsored by your stellar quest account.
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

# 4. Create an Account with 0 XLM balance.
print("Building Transaction...")

transaction = (
    TransactionBuilder (
        source_account = server.load_account(account_id = QUEST_PK),
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee = 100
    )
    .append_begin_sponsoring_future_reserves_op(
        sponsored_id = RANDOM_PK
    )
    .append_create_account_op(
        destination = RANDOM_PK,
        starting_balance = "0"
    )
    .append_end_sponsoring_future_reserves_op(
        source = RANDOM_PK
    )
    .set_timeout(30)
    .build()
)

print("Signing Transaction...")
transaction.sign(QUEST_SK)
transaction.sign(RANDOM_SK)
response = server.submit_transaction(transaction)

print(f"This is the Final Response: {response}")
