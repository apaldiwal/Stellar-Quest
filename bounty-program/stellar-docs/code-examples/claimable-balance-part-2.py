# Method 1: Not available in the Python SDK yet.

# Method 2: Not available in the Python SDK yet.

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

balance_id = balances["_embedded"]["records"][0]["id"]
print(f"Balance ID: {balance_id}")
