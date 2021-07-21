"""
Quest Description:
Create a claimable balance that is only claimable by you and only claimable
after the next challenge. Additionally, the claimable balance must be denoted
in the native XLM asset for an exact amount of 100 XLM.
"""

# 1. Import Libraries
print("Importing Libraries...")

import requests
from stellar_sdk import Server, Keypair, TransactionBuilder, Network
from stellar_sdk import Claimant, ClaimPredicate, Asset

# 2. Load Stellar Quest Keypair
print("Loading Stellar Quest Keypair...")

server = Server("https://horizon-testnet.stellar.org")
QUEST_KEYPAIR = Keypair.from_secret("Enter Your Stellar Quest Secret Key")
QUEST_PK = QUEST_KEYPAIR.public_key
QUEST_SK = QUEST_KEYPAIR.secret

# 3. Create a Claimant Object
print("Creating a Claimant Object...")

# Convert UTC timestamp of next challenge to UNIX timestamp
predicate = ClaimPredicate.predicate_not(
    ClaimPredicate.predicate_before_absolute_time(1609189200)
)

claimant = Claimant (
    destination = QUEST_PK,
    predicate = predicate
)

# 4. Create a ClaimableBalanceEntry
print("Building Transaction...")

transaction = (
    TransactionBuilder (
        source_account = server.load_account(account_id = QUEST_PK),
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee = 100
    )
    .append_create_claimable_balance_op (
        asset = Asset.native(),
        amount = "100",
        claimants = [claimant]
    )
    .set_timeout(30)
    .build()
)

print("Signing Transaction...")
transaction.sign(QUEST_SK)
response = server.submit_transaction(transaction)

print(f"This is the Final Response: {response}")
