package main

import (
	"fmt"
	"log"

	"github.com/stellar/go/clients/horizonclient"
)

func main() {
	client := horizonclient.DefaultPublicNetClient
	offerRequest := horizonclient.OfferRequest {
		OfferID: "165563085",
	}

	resp, err := client.Offers(offerRequest)
	if err != nil {
		log.Fatal(err)
		return
	}
	fmt.Println(resp)
}
