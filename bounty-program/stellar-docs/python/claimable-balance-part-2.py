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
