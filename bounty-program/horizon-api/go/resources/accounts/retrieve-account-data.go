package main

import (
    "fmt"
    "log"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
    accountRequest := horizonclient.AccountRequest {
        AccountID: "GCAXBKU3AKYJPLQ6PEJ6L47KOATCYCBJ2NFRGAK7FUUA2DCEUC265SU2",
        DataKey: "config.memo_required",
    }

    resp, err := client.AccountData(accountRequest)
    if err != nil {
        log.Fatal(err)
        return
    }
    fmt.Println(resp)
}
