from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import jwt
from datetime import datetime, timedelta
import json
from connect import execute_insert, create_connect, execute_query
import os
import uuid

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

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

dataBase = r'./BDloja.DB'

def findUserDB(email: str, password: str):
    conn = create_connect(dataBase)
    query = f"""
    select 1
    from cadastro
    where email = "{email}" AND password = "{password}"
    """
    retorno = execute_query(conn, query)
    if len(retorno) > 0:
        return email
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

def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=403, detail="Invalid token")
    
    
def getToken(request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token not exist")
    
    token = token.replace("Bearer ", "") if "Bearer " in token else token
    
    if not validate_token(token):
        raise HTTPException(status_code=403, detail="Invalid token") 


@app.post("/login")
async def login(request: Request):
    retorno = await request.body()
    retorno = retorno.decode()
    data = json.loads(retorno)
    conn = create_connect(dataBase)
    query = f"""
    select id, firstName, lastName, email
    from cadastro
    where email = '{data['email']}'
    """
    retorno = execute_query(conn, query)
    user = findUserDB(data['email'], data['password'])
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": retorno[0][0], "name": retorno[0][1] + ' ' + retorno[0][2], "email": retorno[0][3]})
    
    conn.close()
    return {"access_token": access_token, "token_type": "bearer", "expire_in_sec": ACCESS_TOKEN_EXPIRE_MINUTES * 60}

@app.post("/sign")
async def cadastro(request : Request):
    data = await request.json()
    conn = create_connect(dataBase)
    query = f"""
    select email
    from cadastro
    where email = "{data['email']}"
    """
    retorno = execute_query(conn, query)
    if len(retorno) == 0:
        query = f"""
        insert into cadastro (id, firstName, lastName, email, phone, password)
        VALUES("{uuid.uuid4()}","{data['firstName']}","{data['lastName']}","{data['email']}","{data['phone']}","{data['password']}")
        """
        execute_insert(conn, query)
    else:
        raise HTTPException(status_code=400, detail="account already exists")

    conn.close()


@app.get('/users')
async def getUsers(request: Request):
    getToken(request)
    conn = create_connect(dataBase)
    query = f"""
    select id, firstName, lastName, email, phone 
    from cadastro
    """
    users = execute_query(conn, query)
    content = []
    for user in users:
        content.append({"id": user[0],"nome": user[1] + ' ' + user[2],"email": user[3],   "phone": user[4]})
    json = {"size": len(users),"content": content}
    
    conn.close()
    return json

@app.put('/users/{id}')
async def changePassword(request: Request, id: str):
    data = await request.json()
    getToken(request)
    conn = create_connect(dataBase)
    check_query = f"""
    select password    
    from cadastro
    Where id = '{id}'
    """
    user = execute_query(conn, check_query)
    if data['atual'] == user[0][0]:
        novasenha = data['novasenha']
        update_query = f"""
        UPDATE cadastro
        SET password = '{novasenha}'
        WHERE id = '{id}'
        """
        execute_query(conn, update_query)
        execute_query(conn, 'commit')
        msg = "Password changed"
        
    else:
        msg = "senhas não conhecidem!"    
        
    conn.close()
    return msg

        
@app.delete('/users/{id}')
async def deleteUser(request: Request, id: str):
    getToken(request)
    conn = create_connect(dataBase)
    check_query = f"""
    select id, firstName, lastName, email, phone    
    from cadastro
    Where id = '{id}'
    """
    user = execute_query(conn, check_query)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    delete_query = f"""
    DELETE
    FROM cadastro
    WHERE id = '{id}'
    """
    execute_query(conn, delete_query)
    execute_query(conn, 'commit')
    
    conn.close()
    return "User deleted successfully"