import pytest
from backend.app import create_app, db

@pytest.fixture
def client():
    app = create_app({
            "TESTING" : True,
            "API_KEY" : "testkey",
            "STORAGE_MODE" : "local",
            "SQLALCHEMY_DATABASE_URI" : "sqlite:///:memory:"
        })

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()