package main

import (
    "fmt"
    "log"

	"github.com/stellar/go/clients/horizonclient"
)

func main() {
	client := horizonclient.DefaultPublicNetClient
	assetRequest := horizonclient.AssetRequest {
		ForAssetCode: "CNY",
	}

	resp, err := client.Assets(assetRequest)
	if err != nil {
		log.Fatal(err)
		return
	}
	fmt.Println(resp)
}
