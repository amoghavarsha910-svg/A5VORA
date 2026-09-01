from .conftest import register_and_token
def test_register_login_and_duplicate(client):
    headers=register_and_token(client)
    assert headers["Authorization"].startswith("Bearer ")
    duplicate=client.post("/api/auth/register",json={"name":"Again","email":"patient@example.com","password":"strong-password","role":"PATIENT"})
    assert duplicate.status_code==400
def test_invalid_password_and_protected_route(client):
    headers=register_and_token(client)
    assert client.post("/api/auth/login",json={"email":"patient@example.com","password":"wrong-password"}).status_code==401
    assert client.get("/api/patients/me").status_code==401
    assert client.get("/api/patients/me",headers=headers).status_code==200

def test_openapi_uses_http_bearer_not_oauth_password_flow(client):
    schemes=client.get("/openapi.json").json()["components"]["securitySchemes"]
    assert schemes["Bearer Authentication"] == {"type":"http","scheme":"bearer","bearerFormat":"JWT"}
