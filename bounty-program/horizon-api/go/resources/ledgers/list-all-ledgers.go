package main

import (
	"fmt"
	"log"

	"github.com/stellar/go/clients/horizonclient"
)

func main() {
	client := horizonclient.DefaultPublicNetClient
	ledgerRequest := horizonclient.LedgerRequest {}

	resp, err := client.Ledgers(ledgerRequest)
	if err != nil {
		log.Fatal(err)
		return
	}
	fmt.Println(resp)
}
