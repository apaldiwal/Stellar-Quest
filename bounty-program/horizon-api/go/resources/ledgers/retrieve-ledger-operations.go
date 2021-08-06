package main

import (
    "fmt"
    "log"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
    operationRequest := horizonclient.OperationRequest {
        ForLedger: uint(27147222),
    }

    resp, err := client.Operations(operationRequest)
    if err != nil {
        log.Fatal(err)
        return
    }
    fmt.Println(resp)
}
