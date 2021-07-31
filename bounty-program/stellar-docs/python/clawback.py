from stellar_sdk import (
    Server,
    Keypair,
    TransactionBuilder,
    Network,
    Asset,
    AuthorizationFlag,
    SetOptions,
    ChangeTrust,
    Payment,
    Clawback
)

server = Server("https://horizon-testnet.stellar.org")

A = Keypair.from_secret("SC7E6KAA7QUOTKFWGFTGTVOHG4DSAEJERIAI3S66MTDUDMINGFCJCQA5")
B = Keypair.from_secret("SB7O2LAIWJGNRLFVJ3PSFU5NBA6XTYWKGAAO5SGC6O2CLQUVVVHMFFWU")
C = Keypair.from_secret("SDE32QTQ5HTDMFJDN4YFQLHBIH5IFJ5X2L6N6A2KK5JFX54GPKUTBGCS")

ASSET = Asset(code = "CLAW", issuer = A.public_key)

# Enables AuthClawbackEnabledFlag on an account.
def enableClawback(account, keys):
    tx = buildTx(
            source = account,
            signer = keys,
            ops = [
                SetOptions(
                    set_flags = AuthorizationFlag.AUTHORIZATION_CLAWBACK_ENABLED |
                        AuthorizationFlag.AUTHORIZATION_REVOCABLE
                )
            ]
    )
    return server.submit_transaction(tx)

# Establishes a trustline for `recipient` for ASSET (from above).
def establishTrustLine(recipient, key):
    tx = buildTx(
            source = recipient,
            signer = key,
            ops = [
                ChangeTrust(
                    asset = ASSET,
                    limit = "5000" # arbitrary
                )
            ]
    )
    return server.submit_transaction(tx)

# Retrieves latest account info for all accounts.
def getAccounts():
    return(
        server.load_account(A.public_key),
        server.load_account(B.public_key),
        server.load_account(C.public_key)
    )

# Enables clawback on A, and establishes trustlines from C, B -> A.
def preamble():
    accountA, accountB, accountC = getAccounts()
    return(
        enableClawback(accountA, A),
        establishTrustLine(accountB, B),
        establishTrustLine(accountC, C)
    )

# Helps simplify creating & signing a transaction.
def buildTx(source, signer, ops):
    tx = (
        TransactionBuilder (
            source_account = source,
            network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee = server.fetch_base_fee()
        )
    )
    for op in ops:
        tx.append_operation(op)
    tx = tx.set_timeout(30).build()
    tx.sign(signer)
    return tx

# Prints the balances of a list of accounts.
def showBalance(accounts):
    for acc in accounts:
        print(acc.account_id[0:5] + ": " + getBalance(acc))

# Make a payment to `toAccount` from `fromAccount` for `amount`.
def makePayment(toAccount, fromAccount, fromKey, amount):
    tx = buildTx(
            source = fromAccount,
            signer = fromKey,
            ops = [
                Payment(
                    destination = toAccount.account_id,
                    asset = ASSET,
                    amount = amount
                )
            ]
    )
    return server.submit_transaction(tx)

# Perform a clawback by `byAccount` of `amount` from `fromAccount`.
def doClawback(byAccount, byKey, fromAccount, amount):
    tx = buildTx(
            source = byAccount,
            signer = byKey,
            ops = [
                Clawback(
                    asset = ASSET,
                    from_ = fromAccount.account_id,
                    amount = amount
                )
            ]
    )
    return server.submit_transaction(tx)

    # Retrieves the balance of ASSET in `account`.
def getBalance(account):
    [(balance.asset_code, balance.asset_issuer) for balance in account.balances]

def examplePaymentClawback():
    accountA, accountB, accountC = getAccounts()
    return(
        makePayment(accountB, accountA, A, "1000"),
        makePayment(accountC, accountB, B, "500"),
        doClawback(accountA, A, accountC, "250")
    )

if __name__ == "__main__":
    preamble()
    examplePaymentClawback()
    showBalances(getAccounts())
