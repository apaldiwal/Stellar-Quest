package main

import (
    "fmt"
    "log"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
    operationRequest := horizonclient.OperationRequest {
        ForLedger: uint(27521176),
    }

    resp, err := client.Payments(operationRequest)
    if err != nil {
        log.Fatal(err)
        return
    }
    fmt.Println(resp)
}
