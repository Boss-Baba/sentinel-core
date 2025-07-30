package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
)

type Verdict struct {
    AlertID     int     `json:"alert_id"`
    ThreatType  string  `json:"threat_type"`
    Confidence  float32 `json:"confidence"`
    Action      string  `json:"action"`
}

// Health check endpoint
func health(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    fmt.Fprintf(w, `{"status": "online", "service": "Response Engine", "version": "1.0"}`)
}

// Handle response requests
func handler(w http.ResponseWriter, r *http.Request) {
    var v Verdict
    err := json.NewDecoder(r.Body).Decode(&v)
    if err != nil {
        http.Error(w, "Bad JSON", http.StatusBadRequest)
        return
    }

    fmt.Printf("[Response] Quarantining endpoint (Alert #%d)\n", v.AlertID)
    log.Printf("✅ Autonomous response executed for Alert #%d", v.AlertID)

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    fmt.Fprintf(w, `{"status": "executed", "alert_id": %d}`, v.AlertID)
}

func main() {
    http.HandleFunc("/", health)                   // ← Health check added
    http.HandleFunc("/api/v1/response", handler)
    fmt.Println("[🛡️ Response Engine] Listening on :9000...")
    log.Fatal(http.ListenAndServe(":9000", nil))
}
