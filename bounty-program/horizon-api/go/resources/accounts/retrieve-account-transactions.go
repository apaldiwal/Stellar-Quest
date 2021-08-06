package main

import (
    "fmt"
    "log"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
    transactionRequest := horizonclient.TransactionRequest {
	   ForAccount: "GAYOLLLUIZE4DZMBB2ZBKGBUBZLIOYU6XFLW37GBP2VZD3ABNXCW4BVA",
	}

    resp, err := client.Transactions(transactionRequest)
	if err != nil {
		log.Fatal(err)
		return
	}
	fmt.Println(resp)
}
