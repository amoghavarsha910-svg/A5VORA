from .conftest import register_and_token
def test_dashboard_empty_and_with_data(client):
    headers=register_and_token(client)
    empty=client.get("/api/dashboard",headers=headers).json()
    assert empty["vitals"]["heart_rate"] is None and empty["alerts"]==[]
    client.post("/api/health/readings",headers=headers,json={"heart_rate":77,"spo2":98,"body_temperature":36.7,"activity":"resting"})
    client.post("/api/environment/readings",headers=headers,json={"ambient_temperature":30,"humidity":50,"air_quality":40})
    data=client.get("/api/dashboard",headers=headers).json()
    assert data["vitals"]["heart_rate"]==77 and data["environment"]["humidity"]==50
def test_patient_data_is_isolated(client):
    first=register_and_token(client,"one@example.com")
    second=register_and_token(client,"two@example.com")
    client.post("/api/health/readings",headers=first,json={"heart_rate":77})
    assert client.get("/api/health/history",headers=second).json()==[]
