"""
Quest Description:
In this challenge, your task is to create an offer to sell your custom asset
for XLM. Stellar's decentralized exchange is a powerful feature that is built
into the core of the protocol. It allows for instant interoperability between
all Stellar assets, including yours!
"""

# 1. Import Libraries
print("Importing Libraries...")

import requests
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset

# 2. Load Stellar Quest Keypair
print("Loading Stellar Quest Keypair...")

server = Server("https://horizon-testnet.stellar.org")
QUEST_KEYPAIR = Keypair.from_secret("Enter Your Stellar Quest Secret Key")
QUEST_PK = QUEST_KEYPAIR.public_key
QUEST_SK = QUEST_KEYPAIR.secret

# 3. Fetch Custom Asset
print("Fetching Custom Asset...")

ISSUING_PK = "Enter Issuing Account Public Key"
asset = Asset(code = "USDC", issuer = ISSUING_PK)

# 4. Manage Sell Offer
print("Building Transaction...")

transaction = (
    TransactionBuilder(
        source_account = server.load_account(account_id = QUEST_PK),
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee = 100
    )
    .append_manage_sell_offer_op(
        selling_code = asset.code,
        selling_issuer = asset.issuer,
        buying_code = "XLM",
        buying_issuer = None,
        amount = "100",
        price = "1",
        offer_id = 0
    )
    .set_timeout(30)
    .build()
)

print("Signing Transaction...")
transaction.sign(QUEST_SK)
response = server.submit_transaction(transaction)

print(f"This is the Final Response: {response}")
