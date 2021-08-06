package main

import (
	"fmt"
	"log"

	"github.com/stellar/go/clients/horizonclient"
)

func main() {
	client := horizonclient.DefaultPublicNetClient

	resp, err := client.TransactionDetail(
		"5ebd5c0af4385500b53dd63b0ef5f6e8feef1a7e1c86989be3cdcce825f3c0cc",
	)
	if err != nil {
		log.Fatal(err)
		return
	}
	fmt.Println(resp)
}
