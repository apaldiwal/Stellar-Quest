package main

import (
	"fmt"
	"log"

	"github.com/stellar/go/clients/horizonclient"
)

func main() {
	client := horizonclient.DefaultPublicNetClient
	offerRequest := horizonclient.OfferRequest {
		Selling: "USD:GDUKMGUGDZQK6YHYA5Z6AY2G4XDSZPSZ3SW5UN3ARVMO6QSRDWP5YLEX",
	}

	resp, err := client.Offers(offerRequest)
	if err != nil {
		log.Fatal(err)
		return
	}
	fmt.Println(resp)
}
