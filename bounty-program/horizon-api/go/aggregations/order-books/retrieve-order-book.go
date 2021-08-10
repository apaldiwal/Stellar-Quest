package main

import (
    "fmt"
    "log"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
    orderBookRequest := horizonclient.OrderBookRequest {
        SellingAssetType: horizonclient.AssetTypeNative,
        BuyingAssetType: horizonclient.AssetType4,
        BuyingAssetCode: "BB1",
        BuyingAssetIssuer: "GD5J6HLF5666X4AZLTFTXLY46J5SW7EXRKBLEYPJP33S33MXZGV6CWFN",
    }

    resp, err := client.OrderBook(orderBookRequest)
    if err != nil {
        log.Fatal(err)
        return
    }
    fmt.Println(resp)
}
