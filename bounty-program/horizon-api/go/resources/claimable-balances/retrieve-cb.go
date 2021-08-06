package main

import (
    "fmt"
    "log"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
    claimableBalanceRequest := horizonclient.ClaimableBalanceRequest {
        ID: "000000000102030000000000000000000000000000000000000000000000000000000000",
    }

    resp, err := client.ClaimableBalances(claimableBalanceRequest)
    if err != nil {
        log.Fatal(err)
        return
    }
    fmt.Println(resp)
}
