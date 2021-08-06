package main

import (
    "fmt"
    "log"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
    claimableBalanceRequest := horizonclient.ClaimableBalanceRequest {
        Asset: "native",
    }

    resp, err := client.ClaimableBalances(claimableBalanceRequest)
    if err != nil {
        log.Fatal(err)
        return
    }
    fmt.Println(resp)
}
