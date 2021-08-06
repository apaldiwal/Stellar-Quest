package main

import (
    "fmt"
    "log"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
    accountRequest := horizonclient.AccountRequest {
        AccountID: "GAYOLLLUIZE4DZMBB2ZBKGBUBZLIOYU6XFLW37GBP2VZD3ABNXCW4BVA",
    }

    resp, err := client.AccountDetail(accountRequest)
    if err != nil {
        log.Fatal(err)
        return
    }
    fmt.Println(resp)
}
