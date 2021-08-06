package main

import (
	"fmt"
	"log"

	"github.com/stellar/go/clients/horizonclient"
)

func main() {
	client := horizonclient.DefaultPublicNetClient
	tradeRequest := horizonclient.TradeRequest {
		BaseAssetType: "credit_alphanum4",
		BaseAssetCode: "USD",
		BaseAssetIssuer: "GDUKMGUGDZQK6YHYA5Z6AY2G4XDSZPSZ3SW5UN3ARVMO6QSRDWP5YLEX",
		CounterAssetType: "native",
	}

	resp, err := client.Trades(tradeRequest)
	if err != nil {
		log.Fatal(err)
		return
	}
	fmt.Println(resp)
}
