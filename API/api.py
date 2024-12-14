from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import jwt
from datetime import datetime, timedelta
import json
from connect import execute_insert, create_connect, execute_query
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# users_db = {
#     "username": "user@example.com",
#     "password": "password123"
# }

# def authenticate_user(username: str, password: str):
#     user = users_db["username"]
#     if not user or users_db["password"] != password:
#         return None
#     if users_db["username"] != username:
#         return None
#     return user

def findUserDB(username: str, password: str):
    dataBase = r'./BDmarcos.DB'
    conn = create_connect(dataBase)
    query = f"""
    select 1
    from cadastro
    where email = "{username}" AND password = "{password}"
    """
    retorno = execute_query(conn, query)
    if len(retorno) > 0:
        return username
    else:
        return None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/login")
async def login(request: Request):
    retorno = await request.body()
    retorno = retorno.decode()
    data = json.loads(retorno)
    user = findUserDB(data['username'], data['password'])
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user})
    return {"access_token": access_token, "token_type": "bearer", "expire_in_sec": ACCESS_TOKEN_EXPIRE_MINUTES * 60}

@app.post("/cadastro")
async def cadastro(request : Request):
    data = await request.json()
    dataBase = r'./BDmarcos.DB'
    conn = create_connect(dataBase)
    query = f"""
    select email
    from cadastro
    where email = "{data['email']}"
    """
    retorno = execute_query(conn, query)
    msg = 0
    if len(retorno) == 0:
        query = f"""
        insert into cadastro (firstName, lastName, email, phone, password)
        VALUES("{data['firstName']}","{data['lastName']}","{data['email']}","{data['phone']}","{data['password']}")
        """
        execute_insert(conn, query)
    else:
        print('Já existe')
        msg = 'jaexiste'

    conn.close()
            
    return msg
