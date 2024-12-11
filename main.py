from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create a FastAPI instance
app = FastAPI()

# Simulated database
users_db = {}

# User model for validation
class User(BaseModel):
    id: int
    name: str
    email: str

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI server!"}

# Get all users
@app.get("/users")
def get_users():
    return {"users": list(users_db.values())}

# Get a single user by ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user}

# Create a new user
@app.post("/users")
def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.id] = user.dict()
    return {"message": "User created successfully", "user": user}

# Update an existing user
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = user.dict()
    return {"message": "User updated successfully", "user": user}

# Delete a user
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted successfully"}
