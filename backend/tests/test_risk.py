from .conftest import register_and_token
def test_rule_based_risk_and_sos(client):
    headers=register_and_token(client)
    client.post("/api/health/readings",headers=headers,json={"heart_rate":120,"spo2":90,"body_temperature":38.5,"fall_detected":False})
    risk=client.get("/api/risk/latest",headers=headers)
    assert risk.status_code==200 and risk.json()["risk_level"]=="HIGH_RISK"
    alerts=client.get("/api/alerts",headers=headers).json()
    assert alerts
    assert client.post(f"/api/alerts/{alerts[0]['id']}/resolve",headers=headers).json()["status"]=="RESOLVED"
    assert client.get("/api/recommendations",headers=headers).json()
    assert client.post("/api/emergency/sos",headers=headers,json={"event_type":"SOS","latitude":12.9716,"longitude":77.5946}).status_code==201
def test_device_ingestion_and_reports(client):
    headers=register_and_token(client)
    response=client.post("/api/device/readings",headers=headers,json={"device_id":"ESP32-001","heart_rate":78,"spo2":98,"ambient_temperature":31,"humidity":58,"air_quality":42})
    assert response.status_code==201
    assert client.get("/api/reports/csv",headers=headers).headers["content-type"].startswith("text/csv")
    assert client.get("/api/reports/pdf",headers=headers).headers["content-type"].startswith("application/pdf")

def test_latest_risk_combines_latest_health_and_environment(client):
    headers=register_and_token(client)
    client.post("/api/health/readings",headers=headers,json={"heart_rate":78,"spo2":98,"body_temperature":36.8,"activity":"walking"})
    client.post("/api/environment/readings",headers=headers,json={"ambient_temperature":31,"humidity":58,"air_quality":42})
    risk=client.get("/api/risk/latest",headers=headers)
    assert risk.status_code==200
    assert risk.json()["confidence"]==0.8
    assert risk.json()["risk_level"]=="NORMAL"
