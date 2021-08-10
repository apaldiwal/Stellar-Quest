package main

import (
    "fmt"
    "log"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient

    resp, err := client.FeeStats()
    if err != nil {
        log.Fatal(err)
        return
    }
    fmt.Println(resp)
}
