import io

def test_delete_file(client):
    upload_response = client.post(
        "/upload",
        headers={"my-api-key": "testkey"},
        data={
            "file": (io.BytesIO(b"fake content"), "delete.jpg")
        },
        content_type="multipart/form-data"
    )

    file_id = upload_response.json["id"]

    delete_response = client.delete(
        f"/delete/{file_id}",
        headers={"my-api-key": "testkey"}
    )

    assert delete_response.status_code == 200
    assert delete_response.json["message"] == "File deleted"