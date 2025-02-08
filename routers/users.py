from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from user_jwt import createToken, validateToken

login_user = APIRouter()


# Es un esquema de validación
class User(BaseModel):
    email: str
    password: str



# Vamos a obtener el token
@login_user.post('/login', tags=['authentication'])
def login(user: User): # si no se cumplen las condiciones devolverá un null
    if user.email == 'briandevita16@gmail.com' and user.password == '123':
        token: str = createToken(user.dict())
        print(token)
        return JSONResponse(content=token)