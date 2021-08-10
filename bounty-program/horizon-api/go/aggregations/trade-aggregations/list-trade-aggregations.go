package main

import (
    "fmt"
    "log"
    "time"

    "github.com/stellar/go/clients/horizonclient"
)

func main() {
    client := horizonclient.DefaultPublicNetClient
    tradeAggregationRequest := horizonclient.TradeAggregationRequest {
        StartTime: time.UnixMilli(int64(1582156800000)) ,
        EndTime: time.UnixMilli(int64(1582178400000)),
        Resolution: horizonclient.HourResolution,
        Offset: 0,
        BaseAssetType: horizonclient.AssetTypeNative,
        CounterAssetType: horizonclient.AssetType4,
        CounterAssetCode: "EURT",
        CounterAssetIssuer: "GAP5LETOV6YIE62YAM56STDANPRDO7ZFDBGSNHJQIYGGKSMOZAHOOS2S",
    }

    resp, err := client.TradeAggregations(tradeAggregationRequest)
    if err != nil {
        log.Fatal(err)
        return
    }
    fmt.Println(resp)
}
