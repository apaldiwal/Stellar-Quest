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

A = Keypair.from_secret("SARQWRSMT5REPFQHNBHSPX7WICDJZZ43GD4YICYBNKIA7WZB3MTHAPZL")
B = Keypair.from_secret("SDFKWXO3WRD5ZHS4G5IZYFOBBUYPMUKFNMK5TTKGIMSGHAZ4CPDGJMM7")
C = Keypair.from_secret("SB7QOMOLKBXGOKE5JUK26ZO5ANPAF7OLE76ZT5Y7MSCK6CYQNVRCQIBR")

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
def establishTrustline(recipient, key):
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
        establishTrustline(accountB, B),
        establishTrustline(accountC, C)
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
def showBalances(accounts):
    for acc in accounts:
        print(acc.account_id()[0:5] + ": " + getBalance(acc))

# Make a payment to `toAccount` from `fromAccount` for `amount`.
def makePayment(toAccount, fromAccount, fromKey, amount):
    tx = buildTx(
            source = fromAccount,
            signer = fromKey,
            ops = [
                Payment(
                    destination = toAccount.account_id(),
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
                    from_ = fromAccount.account_id(),
                    amount = amount
                )
            ]
    )
    return server.submit_transaction(tx)

    # Retrieves the balance of ASSET in `account`.
def getBalance(account):
    balances = server \
        .accounts() \
        .account_id(account.account_id()) \
        .call()["balances"]

    for i in range(len(balances)):
        if balances[i].get("asset_code") == ASSET.code and balances[i].get("asset_issuer") == ASSET.issuer:
            return balances[i]["balance"]
    return "0"

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
