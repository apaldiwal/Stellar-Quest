"""
Quest Description:
Create a custom asset and send it to your account. In this challenge, your task
is to create and send a custom asset to your Stellar Quest account.
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

# 3. Generate Issuing Account Keypair
print("Generating Issuing Account Keypair...")

ISSUING_KEYPAIR = Keypair.random()
ISSUING_PK = ISSUING_KEYPAIR.public_key
ISSUING_SK = ISSUING_KEYPAIR.secret

# 4. Fund Issuing Account via FriendBot
print("Funding Issuing Account...")

FRIENDBOT_URL = "https://friendbot.stellar.org"
response = requests.get(FRIENDBOT_URL, params={'addr': ISSUING_PK})
print(f"FriendBot responded with {response}")

print("")
print("Issuing Account Credentials...")
print(f'Public key: {ISSUING_PK}')
print(f'Private key: {ISSUING_SK}')
print("")

# 7. Create Custom Asset
print("Creating a Custom Asset...")
asset = Asset(code = "USDC", issuer = ISSUING_PK)

# 8. Issue Custom Asset
print("Building Transaction...")

transaction = (
    TransactionBuilder(
        source_account = server.load_account(account_id = QUEST_PK),
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee = 100
    )
    .append_change_trust_op(
        asset_issuer = asset.issuer,
        asset_code = asset.code
    )
    .append_payment_op(
        destination = QUEST_PK,
        amount = "1000",
        asset_code = asset.code,
        asset_issuer = asset.issuer,
        source = ISSUING_PK
    )
    .set_timeout(30)
    .build()
)

print("Signing Transaction...")
transaction.sign(QUEST_SK)
transaction.sign(ISSUING_SK)
response = server.submit_transaction(transaction)

print(f"This is the Final Response: {response}")
