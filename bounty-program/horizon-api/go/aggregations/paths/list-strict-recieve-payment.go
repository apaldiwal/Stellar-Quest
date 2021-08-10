package main

import (
    "fmt"
    "log"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
    pathsRequest := horizonclient.PathsRequest {
        DestinationAssetType: horizonclient.AssetType4,
        DestinationAssetCode: "BB1",
        DestinationAssetIssuer: "GD5J6HLF5666X4AZLTFTXLY46J5SW7EXRKBLEYPJP33S33MXZGV6CWFN",
        DestinationAmount: "5",
        SourceAssets: "CNY:GAREELUB43IRHWEASCFBLKHURCGMHE5IF6XSE7EXDLACYHGRHM43RFOX",
    }

    resp, err := client.StrictReceivePaths(pathsRequest)
    if err != nil {
        log.Fatal(err)
        return
    }
    fmt.Println(resp)
}
