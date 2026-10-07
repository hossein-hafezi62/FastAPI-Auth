from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from jose import jwt, JWTError
from pwdlib import PasswordHash


app = FastAPI()


# ========== Configuration ==========

SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"


# ========== Password Hashing ==========

password_hash = PasswordHash.recommended()


# ========== Database(fake) ==========

fake_users_db = {}


# ========== Schemas / Models ==========

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    username: str
    role: str


# ========== Security ==========

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ========== Helper Functions ==========

def get_user(username: str):
    return fake_users_db.get(username)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = get_user(username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


# ========== Routes ==========

@app.post("/register", status_code=201)
def register(data: RegisterRequest):

    if data.username in fake_users_db:
        raise HTTPException(
            status_code=400,
            detail="username already exists"
        )

    hashed_password = password_hash.hash(data.password)

    fake_users_db[data.username] = {
        "username": data.username,
        "password": hashed_password,
        "role": "user"
    }

    return {
        "message": "User registered successfully"
    }


@app.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends()):

    user = fake_users_db.get(data.username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not password_hash.verify(data.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = jwt.encode(
        {"sub": user["username"]},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/profile", response_model=UserResponse)
def profile(current_user = Depends(get_current_user)):
    return current_user