package main

import (
    "fmt"
    "log"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
    sequence := uint32(69858)

    resp, err := client.LedgerDetail(sequence)
    if err != nil {
        log.Fatal(err)
        return
    }
    fmt.Println(resp)
}
