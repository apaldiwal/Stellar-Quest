package main

import (
	"fmt"
	"log"

	"github.com/stellar/go/clients/horizonclient"
)

func main() {
	client := horizonclient.DefaultPublicNetClient
	operationRequest := horizonclient.OperationRequest {
		ForTransaction: "6b983a4e0dc3c04f4bd6b9037c55f70a09c434dfd01492be1077cf7ea68c2e4a",
	}

	resp, err := client.Operations(operationRequest)
	if err != nil {
		log.Fatal(err)
		return
	}
	fmt.Println(resp)
}
