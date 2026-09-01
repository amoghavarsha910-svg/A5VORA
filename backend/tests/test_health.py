from .conftest import register_and_token
def test_profile_and_health_environment_history(client):
    headers=register_and_token(client)
    assert client.get("/api/patients/me",headers=headers).status_code==200
    assert client.put("/api/patients/me",headers=headers,json={"age":24,"baseline_heart_rate":70}).status_code==200
    health=client.post("/api/health/readings",headers=headers,json={"heart_rate":78,"spo2":98,"body_temperature":36.8,"activity":"walking"})
    assert health.status_code==201
    assert client.get("/api/health/latest",headers=headers).json()["heart_rate"]==78
    assert len(client.get("/api/health/history?limit=5",headers=headers).json())==1
    env=client.post("/api/environment/readings",headers=headers,json={"ambient_temperature":31,"humidity":58,"air_quality":42})
    assert env.status_code==201
    assert client.get("/api/environment/latest",headers=headers).json()["humidity"]==58
    assert len(client.get("/api/environment/history",headers=headers).json())==1
