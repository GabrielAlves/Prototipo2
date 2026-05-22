import io

def test_upload_success(client):
    response = client.post(
        "/upload",
        headers = {"my-api-key" : "testkey"},
        data = {
            "file" : (io.BytesIO(b"fake image content"), "test.jpg")
        },

        content_type = "multipart/form-data"
    )

    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["message"] == "File uploaded"

def test_upload_without_file(client):
    response = client.post(
        "/upload",
        headers={"my-api-key": "testkey"},
        data={},
    )

    assert response.status_code == 400
    assert response.json["error"] == "no file provided"

def test_upload_without_api_key(client):
    response = client.post(
        "/upload",
        data={
            "file": (io.BytesIO(b"fake content"), "test.jpg")
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 401