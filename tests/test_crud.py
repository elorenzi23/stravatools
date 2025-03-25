from app import crud, schemas
from app.models import User

def test_create_user(db):
    user_data = schemas.UserCreate(name="testuser")
    user = crud.create_user(db, user_data)
    assert user.name == "testuser"
