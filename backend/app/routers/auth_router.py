from fastapi import APIRouter, HTTPException, Depends
from app.schemas.pydantic.user_schema import SignupSchema, LoginSchema
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.database import get_db
from bson import ObjectId

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
async def signup(payload: SignupSchema, db=Depends(get_db)):
    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    user = await db.users.find_one({"username": payload.username})
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(payload.password)

    doc = {
        "username": payload.username,
        "email": payload.email,
        "password": hashed,
        "role": payload.role.value
    }

    result = await db.users.insert_one(doc)

    return {"message": "User created", "user_id": str(result.inserted_id)}

@router.post("/login")
async def login(data: LoginSchema, db=Depends(get_db)):
    # 1. Extract username and password safely
    username = data.username
    password = data.password  # <-- Always defined here

    # 2. Find user
    user = await db["users"].find_one({"username": username})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # 3. Verify password
    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # 4. Generate token
    access_token = create_access_token({"sub": str(user["_id"]), "role": user["role"]})

    return {"access_token": access_token, "token_type": "bearer"}
