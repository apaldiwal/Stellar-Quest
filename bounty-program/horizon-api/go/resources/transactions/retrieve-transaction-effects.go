package main

import (
	"fmt"
	"log"

	"github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
	effectRequest := horizonclient.EffectRequest {
		ForTransaction: "512a9946bc7ff4a363299f14f79e0beb9b9cdbd0103e3a69a44446a0aa6471a8",
	}

	resp, err := client.Effects(effectRequest)
	if err != nil {
		log.Fatal(err)
		return
	}
	fmt.Println(resp)
}
