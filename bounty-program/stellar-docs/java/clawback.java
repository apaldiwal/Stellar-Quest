import org.stellar.sdk.*;
import org.stellar.sdk.responses.AccountResponse;
import org.stellar.sdk.responses.SubmitTransactionResponse;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class Clawback {

    static Server server = new Server("https://horizon-testnet.stellar.org");

    static KeyPair A = KeyPair.fromSecretSeed("SCF3XYHHYI6CMVXMKU7AQKUU5F7F6MFEC6CXKM4C44YKYLFKBZRLMBME");
    static KeyPair B = KeyPair.fromSecretSeed("SA5LIXGGDSSMT3QJU6GEYV2XMN5U3QTJNRNQAAIX5M7TOZN5A6KDR5BJ");
    static KeyPair C = KeyPair.fromSecretSeed("SDFIA4SZTPJNEMYLXRZTIWO3T5IG7SF43SMKCVEBRE7S2BKW6FFKJTMX");

    static Asset ASSET = Asset.createNonNativeAsset("CLAW", A.getAccountId());

    // Enables AuthClawbackEnabledFlag on an account.
    static SubmitTransactionResponse enableClawback(TransactionBuilderAccount account, KeyPair keys) {
        try {
            List<Operation> operationList = new ArrayList<>();
            operationList.add(
                    new SetOptionsOperation.Builder()
                            .setSetFlags(2 | 8)
                            .build()
            );
            Transaction tx = buildTx(account, keys, operationList);
            return server.submitTransaction(tx);
        }
        catch (IOException | AccountRequiresMemoException e) {
            e.printStackTrace();
            return null;
        }
    }

    /// Establishes a trustline for `recipient` for ASSET (from above).
    static SubmitTransactionResponse establishTrustline(TransactionBuilderAccount recipient, KeyPair key) {

        try {
            List<Operation> operationList = new ArrayList<>();
            operationList.add(
                    new ChangeTrustOperation.Builder(ASSET, "5000").build()
            );
            Transaction tx = buildTx(recipient, key, operationList);
            return server.submitTransaction(tx);
        }
        catch (IOException | AccountRequiresMemoException e) {
            e.printStackTrace();
            return null;
        }
    }

    /// Retrieves the latest account info for all accounts.
    static TransactionBuilderAccount[] getAccounts() {
        try {
            return new TransactionBuilderAccount[]{
                    server.accounts().account(A.getAccountId()),
                    server.accounts().account(B.getAccountId()),
                    server.accounts().account(C.getAccountId())
            };
        }
        catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    /// Enables clawback on A, and establishes trustlines from C, B -> A.
    static void preamble() {

        TransactionBuilderAccount accountA = getAccounts()[0];
        TransactionBuilderAccount accountB = getAccounts()[1];
        TransactionBuilderAccount accountC = getAccounts()[2];

        enableClawback(accountA, A);
        establishTrustline(accountB, B);
        establishTrustline(accountC, C);
    }

    /// Helps simplify creating & signing a transaction.
    static Transaction buildTx(TransactionBuilderAccount source, KeyPair signer, List<Operation> ops) {
        Transaction.Builder txBuilder = new Transaction.Builder(source, Network.TESTNET)
                .setBaseFee(Transaction.MIN_BASE_FEE);
        for (Operation op : ops) {
            txBuilder.addOperation(op);
        }
        Transaction tx = txBuilder.setTimeout(30).build();
        tx.sign(signer);
        return tx;
    }

    /// Prints the balances of a list of accounts.
    static void showBalances(TransactionBuilderAccount[] accounts) {
        for(TransactionBuilderAccount account: accounts)
            System.out.println(account.getAccountId().substring(0, 5) + ": "
                    + Float.parseFloat(getBalance(account)));
    }

    /// Make a payment to `toAccount` from `fromAccount` for `amount`.
    static SubmitTransactionResponse makePayment(TransactionBuilderAccount toAccount,
                                                 TransactionBuilderAccount fromAccount, KeyPair fromKey,
                                                 String amount) {
        try {
            List<Operation> operationList = new ArrayList<>();
            operationList.add(
                    new PaymentOperation.Builder(
                            toAccount.getAccountId(), ASSET, amount).build()
            );
            Transaction tx = buildTx(fromAccount, fromKey, operationList);
            return server.submitTransaction(tx);
        }
        catch (IOException | AccountRequiresMemoException e) {
            e.printStackTrace();
            return null;
        }
    }

    /// Perform a clawback by `byAccount` of `amount` from `fromAccount`.
    static SubmitTransactionResponse doClawback(TransactionBuilderAccount byAccount, KeyPair byKey,
                                                TransactionBuilderAccount fromAccount, String amount) {
        try {
            List<Operation> operationList = new ArrayList<>();
            operationList.add(
                    new ClawbackOperation.Builder(
                            fromAccount.getAccountId(), ASSET, amount).build()
            );
            Transaction tx = buildTx(byAccount, byKey, operationList);
            return server.submitTransaction(tx);
        }
        catch (IOException | AccountRequiresMemoException e) {
            e.printStackTrace();
            return null;
        }
    }

    /// Retrieves the balance of ASSET in `account`.
    static String getBalance(TransactionBuilderAccount account) {
        try {
            AccountResponse.Balance[] balances = server.accounts()
                    .account(account.getAccountId()).getBalances();

            for(AccountResponse.Balance balance: balances) {
                if(Objects.equals(balance.getAssetCode(), "CLAW")
                        && Objects.equals(balance.getAssetIssuer(), A.getAccountId())) {
                    return balance.getBalance();
                }
            }
        }
        catch (IOException e) {
            e.printStackTrace();
        }
        return "0";
    }

    static void examplePaymentClawback() {
        TransactionBuilderAccount accountA = getAccounts()[0];
        TransactionBuilderAccount accountB = getAccounts()[1];
        TransactionBuilderAccount accountC = getAccounts()[2];

        makePayment(accountB, accountA, A, "1000");
        makePayment(accountC, accountB, B, "500");
        doClawback( accountA, A, accountC, "250");

        showBalances(getAccounts());
    }

    public static void main(String[] args) {
        preamble();
        examplePaymentClawback();
    }
}
