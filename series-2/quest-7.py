"""
Quest Description:
Revoke account sponsorship for the account you're sponsoring. Remember that
account you sponsored in the last challenge? Well the winds of change are
blowing and you no longer wish to sponsor their absolute minimum balance any
longer. In this challenge you need to revoke account sponsorship for the
account you're currently sponsoring.
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

# 3. Load Sponsored Account Keypair
print("Loading Sponsored Account Keypair...")

SPONSORED_PK = "Enter Your Sponsored Account Public Key"

# 4. Revoke Account Sponsorship
print("Building Transaction...")

transaction = (
    TransactionBuilder(
        source_account = server.load_account(account_id = QUEST_PK),
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee = 100
    )
    .append_payment_op(
        destination = SPONSORED_PK,
        amount = "1",
        asset_code = "XLM"
    )
    .append_revoke_account_sponsorship_op(
        account_id = SPONSORED_PK
    )
    .set_timeout(30)
    .build()
)

print("Signing Transaction...")
transaction.sign(QUEST_SK)
response = server.submit_transaction(transaction)

print(f"This is the Final Response: {response}")
