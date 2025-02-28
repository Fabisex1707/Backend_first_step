#Crud basico con una base de datos falsa, usa postman o thunderclient para realizar las peubas pertinentes, asi como revisar la documentacion -->dicIP/docs 
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm #EL primero hace la autenticacion, nos da el formato para recibir y enviar los datos de la autenticacion
basic_crud=APIRouter()

outh2= OAuth2PasswordBearer(tokenUrl='Login')

class User(BaseModel):
    username:str
    full_name:str
    email:str
    disabled:bool

class UserDB(User):
    password:str

def research_user(username:str):
    if username in users_db:
        return User(**users_db[username])

def research_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])

def current_user_db(token:Annotated[str,Depends(outh2)]):
    user=research_user_db(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail='No existe el usario'
        )
    return user

def current_user(token:Annotated[str,Depends(outh2)]):
    user=research_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail='No existe el usario'
        )
    return user

users_db={
    'Fabian':{
        'username':"Fabisex",
        'full_name':'Fabian Castro Dolores',
        'email':'Camikami1707@xd.com',
        'disabled':False,
        'password':'123456'
    },
    'Fabi_2':{
        'username':"Fabisex_2",
        'full_name':'Fabian Castro D',
        'email':'Camikami1707@xd.com',
        'disabled':True,
        'password':'abcdefg'
    },
    'Violeta':{
        'username':"Fabisex_2",
        'full_name':'Fabian Castro D',
        'email':'Camikami1707@xd.com',
        'disabled':True,
        'password':'xd1707'
    }
}



@basic_crud.post('/login')
async def login(form:Annotated[OAuth2PasswordRequestForm,Depends()]):
    userdb=users_db.get(form.username)
    user=research_user_db(form.username)
    if not userdb:
        raise HTTPException(status_code=400,detail='El usario no es correcto')
    if not form.password==user.password:
        raise HTTPException(status_code=400,detail='La contrasena no es correcta')

    return {'acces_token': user.username,'token_type':'bearer'}

@basic_crud.get('/users/mee')
async def me(user:Annotated[User,Depends(current_user)]): #al poner criterios de dependencia le decimos al back que la unica form ade realizar esa opracion es primero validando que ese susario si esta registrado
    return user


@basic_crud.post('/register/{key}')
async def register(user: UserDB,key:str):
    if key in users_db:
        raise HTTPException(
            status_code=400,
            detail='El usuario ya está registrado'
        )
    users_db[key] = {
    "username": user.username,
    "full_name": user.full_name,
    "email": user.email,
    "disabled": user.disabled,
    "password": user.password
    }
    return users_db

@basic_crud.put('/update/{key}',status_code=status.HTTP_200_OK)
async def update(user:UserDB,key:str):
    found=False
    for x in users_db:
        if x == key:
            users_db[key] = {
                "username": user.username,
                "full_name": user.full_name,
                "email": user.email,
                "disabled": user.disabled,
                "password": user.password
                }
            found=True
            return {"Message":"Usario actualizado"}
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No se encontro el usario')

@basic_crud.delete('/borrar/{key}',status_code=status.HTTP_200_OK)
async def vanish(key:str):
    found=False
    for x in users_db:
        if x == key:
            del (users_db[key])
            found=True
            return users_db
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No se encontro el usario')

    
    
    
    












