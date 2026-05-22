import io

def test_list_empty(client):
    response = client.get(
        "/list",
        headers = {"my-api-key" : "testkey"}
    )

    assert response.status_code == 200
    assert response.json == []

def test_list_after_upload(client):
    client.post(
        "/upload",
        headers={"my-api-key": "testkey"},
        data={
            "file": (io.BytesIO(b"fake content"), "image.jpg")
        },
        content_type="multipart/form-data"
    )

    response = client.get(
        "/list",
        headers={"my-api-key": "testkey"}
    )

    assert response.status_code == 200
    assert len(response.json) == 1