package main

import (
    "fmt"
	"log"

	"github.com/stellar/go/clients/horizonclient"
)

func main() {
	client := horizonclient.DefaultPublicNetClient
	accountsRequest := horizonclient.AccountsRequest {
		Signer: "GBPOFUJUHOFTZHMZ63H5GE6NX5KVKQRD6N3I2E5AL3T2UG7HSLPLXN2K",
	}

	resp, err := client.Accounts(accountsRequest)
	if err != nil {
		log.Fatal(err)
		return
	}
	fmt.Println(resp)
}
