claimBalance = ClaimClaimableBalance(balance_id = balance_id)
print(f"{A.public_key} claiming {balance_id}")

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
