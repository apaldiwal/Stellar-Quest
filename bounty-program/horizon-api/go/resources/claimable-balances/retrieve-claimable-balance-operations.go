package main

import (
    "fmt"
    "log"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
    operationRequest := horizonclient.OperationRequest {
        ForClaimableBalance: "00000000178826fbfe339e1f5c53417c6fedfe2c05e8bec14303143ec46b38981b09c3f9",
    }

    resp, err := client.Operations(operationRequest)
    if err != nil {
        log.Fatal(err)
        return
    }
    fmt.Println(resp)
}
