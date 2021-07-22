"""
Quest Description:
Claim your claimable balance. Remember that claimable balance you setup in
the last challenge? This challenge is to simply claim that balance and
get your XLM back.
"""

# 1. Import Libraries
print("Importing Libraries...")

import requests
from stellar_sdk import Server, Keypair, TransactionBuilder, Network
from stellar_sdk import Claimant, ClaimPredicate, Asset
from stellar_sdk.exceptions import BadResponseError, BadRequestError

# 2. Load Stellar Quest Keypair
print("Loading Stellar Quest Keypair...")

server = Server("https://horizon-testnet.stellar.org")
QUEST_KEYPAIR = Keypair.from_secret("Enter Your Stellar Quest Secret Key")
QUEST_PK = QUEST_KEYPAIR.public_key
QUEST_SK = QUEST_KEYPAIR.secret

# 3. Get Claimable Balance ID
print("Retrieving Claimable Balance ID...")

try:
    balances = (
        server
        .claimable_balances()
        .for_claimant(QUEST_PK)
        .limit(1)
        .order(desc = True)
        .call()
    )
except (BadRequestError, BadResponseError) as err:
    print(f"Claimable Balance Retrieval Failed: {err}")

balance_id = balances["_embedded"]["records"][0]["id"]
print(f"Claimable Balance ID: {balance_id}")

# 4. Create a ClaimableBalanceEntry
print("Building Transaction...")

transaction = (
    TransactionBuilder(
        source_account = server.load_account(account_id = QUEST_PK),
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee = 100
    )
    .append_claim_claimable_balance_op(
        balance_id = balance_id
    )
    .set_timeout(30)
    .build()
)

print("Signing Transaction...")
transaction.sign(QUEST_SK)
response = server.submit_transaction(transaction)

print(f"This is the Final Response: {response}")
