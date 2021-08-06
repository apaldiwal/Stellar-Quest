package main

import (
	"fmt"
	"log"

	"github.com/stellar/go/clients/horizonclient"
)

func main() {
	client := horizonclient.DefaultPublicNetClient
	transactionRequest := horizonclient.TransactionRequest {
		ForLedger: uint(27147222),
	}

	resp, err := client.Transactions(transactionRequest)
	if err != nil {
		log.Fatal(err)
		return
	}
	fmt.Println(resp)
}
