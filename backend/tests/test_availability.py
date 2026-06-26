from frontend.app import app as frontend_app


# def test_backend_available(client):
#     response = client.get("/health")

#     assert response.status_code == 200
#     assert response.json == {"status": "ok"}


# def test_frontend_available():
#     frontend_client = frontend_app.test_client()
#     response = frontend_client.get("/")

#     assert response.status_code == 200
#     assert b"<!doctype html>" in response.data.lower()