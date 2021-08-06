package main

import (
    "fmt"
    "log"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
    operationRequest := horizonclient.OperationRequest {
	   ForAccount: "GCNL55IJTH2HX26HLNIGYD2JIQLTBAQL3SVPNZA6PXK7NAVHU423WOTE",
    }

    resp, err := client.Payments(operationRequest)
    if err != nil {
        log.Fatal(err)
        return
    }
    fmt.Println(resp)
}
