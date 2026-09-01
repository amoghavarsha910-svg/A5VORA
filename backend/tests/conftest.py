import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

@pytest.fixture()
def client(tmp_path):
    engine=create_engine(f"sqlite:///{tmp_path / 'test.db'}",connect_args={"check_same_thread":False})
    TestingSession=sessionmaker(autocommit=False,autoflush=False,bind=engine)
    Base.metadata.create_all(bind=engine)
    def override_db():
        db=TestingSession()
        try: yield db
        finally: db.close()
    app.dependency_overrides[get_db]=override_db
    with TestClient(app) as test_client: yield test_client
    app.dependency_overrides.clear(); Base.metadata.drop_all(bind=engine)

def register_and_token(client,email="patient@example.com",password="strong-password"):
    response=client.post("/api/auth/register",json={"name":"Test Patient","email":email,"password":password,"role":"PATIENT"})
    assert response.status_code==201,response.text
    login=client.post("/api/auth/login",json={"email":email,"password":password})
    assert login.status_code==200,login.text
    return {"Authorization":f"Bearer {login.json()['access_token']}"}
