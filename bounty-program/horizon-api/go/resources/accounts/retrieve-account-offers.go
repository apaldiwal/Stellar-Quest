package main

import (
    "fmt"
    "log"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
    offerRequest := horizonclient.OfferRequest {
        ForAccount: "GD3CJYUTZAY6JQF4CEI6Z7VW5O6VNGKZTBYUECTOJPEDTB7I2HZSPI2K",
    }

    resp, err := client.Offers(offerRequest)
    if err != nil {
        log.Fatal(err)
        return
    }
    fmt.Println(resp)
}
