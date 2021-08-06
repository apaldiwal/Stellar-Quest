package main

import (
    "fmt"
    "log"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
    effectRequest := horizonclient.EffectRequest {
        ForLedger: "0",
    }

    resp, err := client.Effects(effectRequest)
    if err != nil {
        log.Fatal(err)
        return
    }
    fmt.Println(resp)
}
