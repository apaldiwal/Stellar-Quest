import time
from stellar_sdk.xdr import TransactionResult, OperationType
from stellar_sdk.exceptions import NotFoundError, BadResponseError, BadRequestError
from stellar_sdk import (
    Keypair,
    Network,
    Server,
    TransactionBuilder,
    Transaction,
    Asset,
    Operation,
    Claimant,
    ClaimPredicate,
    CreateClaimableBalance,
    ClaimClaimableBalance
)

server = Server("https://horizon-testnet.stellar.org")

A = Keypair.from_secret("SBDLSAHWZHQZG6ZQDJY63XQORETH5X5Q5BM66JUW4E6S7CVHXGX373GO")
B = Keypair.from_public_key("GBS6YWU5NAFZFZTRYMVVRBGE4IREF67AYVC3EFYMKS5NZVCHX2NXFB6L")

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

# Method 1: Not available in the Python SDK yet.

# Method 2: Suppose `txResponse` comes from the transaction submission
# above.
txResult = TransactionResult.from_xdr(txResponse["result_xdr"])
results = txResult.result.results

# We look at the first result since our first (and only) operation
# in the transaction was the CreateClaimableBalanceOp.
operationResult = results[0].tr.create_claimable_balance_result
balanceId = operationResult.balance_id.to_xdr_bytes().hex()
print(f"Balance ID (2): {balanceId}")

# Method 3: Account B could alternatively do something like:
try:
    balances = (
        server
        .claimable_balances()
        .for_claimant(B.public_key)
        .limit(1)
        .order(desc = True)
        .call()
    )
except (BadRequestError, BadResponseError) as err:
    print(f"Claimable balance retrieval failed: {err}")

balanceId = balances["_embedded"]["records"][0]["id"]
print(f"Balance ID (3): {balanceId}")

claimBalance = ClaimClaimableBalance(balance_id = balanceId)
print(f"{A.public_key} claiming {balanceId}")

tx = (
    TransactionBuilder (
        source_account = aAccount,
        network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee = server.fetch_base_fee()
    )
    .append_operation(claimBalance)
    .set_timeout(180)
    .build()
)

tx.sign(A)
try:
    txResponse = server.submit_transaction(tx)
except (BadRequestError, BadResponseError) as err:
    print(f"Tx submission failed: {err}")
