from fastapi.testclient import TestClient
from src.api.main import app 

clinet = TestClient(app)

def test_get_all_products():
    response = clinet.get("/products?skip=0&limit=5")

    assert response.status_code == 200

    assert isinstance(response.json(), list)

def test_analytics_top_products():
    response = clinet.get("/analytics/top-products")

    assert response.status_code == 200

    data = response.json()

    if len(data)>= 0:
        assert "total_comments" in data[0]

def test_ai_semantic_search():
    response = clinet.get("/search/comments?query=باتری&limit=1")
    
    assert response.status_code == 200

    assert isinstance(response.json(), list)
    
