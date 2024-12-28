from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import jwt
from datetime import datetime, timedelta
import json
from connectmySQL import execute_insert, create_connect, execute_query
import os
import uuid
import BD

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

dataBase = BD.db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# procura usuario no banco
def findUserDB(email: str, password: str):
    conn = create_connect(BD.banco)
    query = f"""
    select 1
    from usuarios
    where email = "{email}" AND password = "{password}"
    """
    retorno = execute_query(conn, query)
    conn.close()
    if len(retorno) > 0:
        return email
    else:
        return None

# cria o token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# valida se token é valido
def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=403, detail="Invalid token")
    
    
# pega o token pelo header do frontEnd
def getToken(request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token not exist")
    
    token = token.replace("Bearer ", "") if "Bearer " in token else token
    
    if not validate_token(token):
        raise HTTPException(status_code=403, detail="Invalid token") 


# faz login
@app.post("/login")
async def login(request: Request):
    retorno = await request.body()
    retorno = retorno.decode()
    data = json.loads(retorno)
    conn = create_connect(BD.banco)
    query = f"""
    select id, firstName, lastName, email
    from usuarios
    where email = '{data['email']}'
    """
    retorno = execute_query(conn, query)
    user = findUserDB(data['email'], data['password'])
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": retorno[0][0], "name": retorno[0][1] + ' ' + retorno[0][2], "email": retorno[0][3]})
    
    conn.close()
    return {"access_token": access_token, "token_type": "bearer", "expire_in_sec": ACCESS_TOKEN_EXPIRE_MINUTES * 60}

# faz cadastro
@app.post("/sign")
async def cadastro(request : Request):
    data = await request.json()
    conn = create_connect(BD.banco)
    query = f"""
    select email
    from usuarios
    where email = "{data['email']}"
    """
    retorno = execute_query(conn, query)
    if len(retorno) == 0:
        query = f"""
        insert into usuarios (id, firstName, lastName, email, phone, password)
        VALUES("{uuid.uuid4()}","{data['firstName']}","{data['lastName']}","{data['email']}","{data['phone']}","{data['password']}")
        """
        execute_insert(conn, query)
    else:
        raise HTTPException(status_code=400, detail="account already exists")
    
    conn.close()
    return {"detail": "Account created"}

# lista todos usuários
@app.get('/users')
async def getUsers(request: Request):
    getToken(request)
    conn = create_connect(BD.banco)
    query = f"""
    select id, firstName, lastName, email, phone 
    from usuarios
    """
    users = execute_query(conn, query)
    content = []
    for user in users:
        content.append({"id": user[0],"nome": user[1] + ' ' + user[2],"email": user[3],   "phone": user[4]})
    if not content:
        raise HTTPException(status_code=404, detail='Unable to fetch users')
    json = {"size": len(users),"content": content}
    
    conn.close()
    return json

# edita usuário
@app.put('/users/{id}')
async def changePassword(request: Request, id: str):
    data = await request.json()
    getToken(request)
    conn = create_connect(BD.banco)
    check_query = f"""
    select password    
    from usuarios
    Where id = '{id}'
    """
    user = execute_query(conn, check_query)
    if data['atual'] == user[0][0]:
        novasenha = data['novasenha']
        update_query = f"""
        UPDATE usuarios
        SET password = '{novasenha}'
        WHERE id = '{id}'
        """
        execute_query(conn, update_query)
        execute_query(conn, 'commit')
        conn.close()
        return {"details": "Password changed"}
    else:
        return {"details": "Passwords do not match"} 

# deleta usuário    
@app.delete('/users/{id}')
async def deleteUser(request: Request, id: str):
    getToken(request)
    conn = create_connect(BD.banco)
    check_query = f"""
    select id, firstName, lastName, email, phone    
    from usuarios
    Where id = '{id}'
    """
    user = execute_query(conn, check_query)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    delete_query = f"""
    DELETE
    FROM usuarios
    WHERE id = '{id}'
    """
    execute_query(conn, delete_query)
    execute_query(conn, 'commit')
    
    conn.close()
    return "User deleted successfully"


#cria produto
@app.post('/products')
async def createProduct(req: Request):
    data = await req.json()
    getToken(req)
    conn = create_connect(BD.banco)
    check_query = f"""
        select sku
        from produtos
        where sku = '{data['sku']}'
    """
    prod = execute_query(conn, check_query)
    if len(prod) == 0:
        insert_query = f"""
        insert into produtos (sku, nome, cor, qtd, preco, img)
        VALUES("{data['sku']}","{data['nome']}","{data['cor']}","{data['qtd']}","{data['preco']}","{data['img']}")
        """
        execute_insert(conn, insert_query)
        
        conn.close()
        return {"details": "Product created successfully"}
    else:
        raise HTTPException(status_code=400, detail='product already registered')
    
#lista produtos
@app.get('/products')
async def getProducts(req: Request):
    conn = create_connect(BD.banco)
    query = f"""
    select sku, nome, cor, qtd, preco, img 
    from produtos
    """
    produtos = execute_query(conn, query)
    content = []
    for produto in produtos:
        content.append({"sku": produto[0],"nome": produto[1], "cor": produto[2], "qtd": produto[3], "preco": produto[4], "img": produto[5]})
    json = {"size": len(produtos),"content": content}
    
    conn.close()
    return json
  
# edita produto
@app.put('/products/{sku}')
async def editProduct(req: Request, sku: str):
    data = await req.json()
    getToken(req)
    conn = create_connect(BD.banco)
    check_query = f"""
    select sku, nome, cor, qtd
    from produtos
    where sku = '{sku}'
    """
    res = execute_query(conn, check_query)
    if not res:
        raise HTTPException(status_code=404, detail='product not found')
    
    update_query = f"""
    UPDATE produtos
    SET sku = '{data['sku']}',nome = '{data['nome']}',cor = '{data['cor']}', qtd = '{data['qtd']}, preco = '{data['preco']}', img = '{data['img']}'
    WHERE sku = '{sku}';
    """
    execute_query(conn, update_query)
    execute_query(conn, 'commit')
    
    conn.close()
    return 'changed product'
    
#exclui produto
@app.delete('/products/{sku}')
async def editProduct(req: Request, sku: str):
    getToken(req)
    conn = create_connect(BD.banco)
    check_query = f"""
    select sku, nome, cor, qtd    
    from produtos
    Where sku = '{sku}'
    """
    produto = execute_query(conn, check_query)
    if not produto:
        raise HTTPException(status_code=404, detail="product not found")
    delete_query = f"""
    DELETE
    FROM produtos
    WHERE sku = '{sku}'
    """
    execute_query(conn, delete_query)
    execute_query(conn, 'commit')
    
    conn.close()
    return {"details": "product deleted successfully"}

#adiciona produto no carrinho
@app.post('/cart/{sku}')
async def addCart(req: Request, sku: str):
    data = await req.json()
    getToken(req)
    conn = create_connect(BD.banco)
    prod_query = f"""
    select sku, qtd, nome, preco, img  
    from produtos
    Where sku = '{sku}'
    """
    produto = execute_query(conn, prod_query)
    if len(produto) > 0:
        cart_query = f"""
        select sku, qtdcart 
        from carrinho
        Where sku = '{sku}' and id = '{data['id']}'
        """
        carrinho = execute_query(conn, cart_query)
        if len(carrinho) > 0:
            if (int(carrinho[0][1]) + data['qtd_compra']) > produto[0][1]:
                raise HTTPException(status_code=404, detail='acabou')
            qtd = carrinho[0][1]
            qtd += data['qtd_compra']
            update_query = f"""
            UPDATE carrinho
            SET qtdcart = '{qtd}'
            WHERE sku = '{sku}' and id = '{data['id']}'
            """
            execute_query(conn, update_query)
            execute_query(conn, 'commit')
        else:
            qtd = produto[0][1]
            qtd_compra = data['qtd_compra']
            if qtd_compra > qtd:
                raise HTTPException(status_code=404, detail='product not in stock')    
            insert_query = f"""
            insert into carrinho (id, sku, qtdcart, nome, preco, img)
            VALUES("{data['id']}", "{sku}", "{qtd_compra}", "{produto[0][2]}", "{produto[0][3]}", "{produto[0][4]}")
            """
            execute_insert(conn, insert_query)
    

#lista o que tem no carrinho
@app.get('/cart/{id}')
async def getProducts(req: Request, id: str):
    getToken(req)
    conn = create_connect(BD.banco)
    query = f"""
    select sku, qtdcart, nome, img, preco
    from carrinho
    where id = '{id}'
    """
    produtos = execute_query(conn, query)
    content = []
    for produto in produtos:
        content.append({"id": id, "sku": produto[0], "qtdcarrinho": produto[1], "nome": produto[2], "img": produto[3], "preco": produto[4]})
    json = {"size": len(produtos),"content": content}
    
    conn.close()
    return json

# deleta produto do carrinho
@app.delete('/cart/{id}/{sku}')
async def deleteProduct(req: Request, id: str, sku: str):
    getToken(req)
    conn = create_connect(BD.banco)
    check_query = f"""
        select id, sku, nome    
        from carrinho
        Where sku = '{sku}' and id = '{id}'
        """
    res = execute_query(conn, check_query)
    if not res:
        raise HTTPException(status_code=404, detail="product not found")
    delete_query = f"""
    DELETE
    FROM carrinho
    WHERE sku = '{sku}' and id = '{id}'
    """
    execute_query(conn, delete_query)
    execute_query(conn, 'commit')
    
    conn.close()
    return {"status": 200, "message": "Product successfully deleted"}  

# deletar todo o carrinho
@app.delete('/cart/{id}')
async def deleteCart(req: Request, id: str):
    getToken(req)
    conn = create_connect(BD.banco)
    delete_query = f"""
        delete
        from carrinho
        where id = '{id}'
    """
    execute_query(conn, delete_query)
    execute_query(conn, 'commit')
    conn.close()
    return {"status": 200, "message": "cart successfully deleted"}