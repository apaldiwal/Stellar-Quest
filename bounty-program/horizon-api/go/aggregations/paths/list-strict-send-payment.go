package main

import (
  "fmt"
  "log"

  "github.com/stellar/go/clients/horizonclient"
)

func main() {
  client := horizonclient.DefaultPublicNetClient
  pathsRequest := horizonclient.StrictSendPathsRequest {
    DestinationAccount: "GAYOLLLUIZE4DZMBB2ZBKGBUBZLIOYU6XFLW37GBP2VZD3ABNXCW4BVA",
    SourceAssetType: horizonclient.AssetType4,
    SourceAssetCode: "BRL",
    SourceAssetIssuer: "GDVKY2GU2DRXWTBEYJJWSFXIGBZV6AZNBVVSUHEPZI54LIS6BA7DVVSP",
    SourceAmount: "400",
  }

  resp, err := client.StrictSendPaths(pathsRequest)
  if err != nil {
    log.Fatal(err)
    return
  }
  fmt.Println(resp)
}
