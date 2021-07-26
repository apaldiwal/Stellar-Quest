from stellar_sdk import Keypair, Network, Server
from stellar_sdk import TransactionBuilder, Transaction, Asset, Operation
from stellar_sdk import Claimant, ClaimPredicate, CreateClaimableBalance, ClaimClaimableBalance
from stellar_sdk.exceptions import NotFoundError, BadResponseError, BadRequestError
import time

server = Server("https://horizon-testnet.stellar.org")

A = Keypair.from_secret("SANRGB5VXZ52E7XDGH2BHVBFZR4S25AUQ4BR7SFXIQYT5J6W2OES2OP7")
B = Keypair.from_public_key("GAAPSRMYNFAO3TDQTLNLKN76IQ3E6IQAKU23PSQX3BIV7RTEBXHQIWU6")

# NOTE: Proper error checks are omitted for brevity; always validate things!

try:
    aAccount = server.load_account(A.public_key)
except NotFoundError:
    raise Exception(f"Failed to load {A.public_key}")

# Create a claimable balance with our two above-described conditions.
soon = int(time.time() + 60)
bCanClaim = ClaimPredicate.predicate_before_relative_time(60)
aCanClaim = ClaimPredicate.predicate_not(
    ClaimPredicate.predicate_before_absolute_time(soon)
)

# Create the operation and submit it in a transaction.
claimableBalanceEntry = CreateClaimableBalance(
    asset = Asset.native(),
    amount = "420",
    claimants = [
        Claimant(destination = B.public_key, predicate = bCanClaim),
        Claimant(destination = A.public_key, predicate = aCanClaim)
    ]
)

tx = (
    TransactionBuilder (
        source_account = aAccount,
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee = server.fetch_base_fee()
    )
    .append_operation(claimableBalanceEntry)
    .set_timeout(180)
    .build()
)

tx.sign(A)
try:
    txResponse = server.submit_transaction(tx)
    print("Claimable balance created!")
except (BadRequestError, BadResponseError) as err:
    print(f"Tx submission failed: {err}")
