from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm #EL primero hace la autenticacion, nos da el formato para recibir y enviar los datos de la autenticacion
app=FastAPI()

outh2= OAuth2PasswordBearer(tokenUrl='Login')

class User(BaseModel):#basemodel= crear una entidad pero sin el constructor usual
    #Path y Qwery
    username:str
    full_name:str
    email:str
    disabled:bool
#apliacion de la herencia en poo
class user_db(User):
    password:str


#En principio os datos se ven asi pues solo es un ajemplo, pero a futuro hay que usar un "hash"
users_db={
    'Fabian':{
        'username':"Fabian",
        'full_name':'Fabian Castro Dolores',
        'email':'Camikami1707@xd.com',
        'disabled':False,
        'password':'123456'
    },
    'Fabi_2':{
        'username':"Fabi_2",
        'full_name':'Fabian Castro D',
        'email':'Camikami1707@xd.com',
        'disabled':True,
        'password':'abcdefg'
    },
    'Violeta':{
        'username':"Violeta",
        'full_name':'Fabian Castro D',
        'email':'Camikami1707@xd.com',
        'disabled':False,
        'password':'xd1707'
    }
}


def search_user_db(username:str):
    if username in users_db:
        return user_db(**users_db[username])
    
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    
async def current_user(token:Annotated[str, Depends(outh2)]):
    user= search_user(token)
    if not user:
        raise HTTPException(status_code=401,
                      detail='Credenciales invalidas',
                      headers={'www-Authenticte':' bearer'})
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Usario inactivo!!!'
        )
    
    return user


@app.post('/login')
async def login(form:Annotated[OAuth2PasswordRequestForm,Depends()]):
    userdb=users_db.get(form.username)

    if not userdb:
        raise HTTPException(status_code=400,detail='El usario no es correcto')
    
    user=search_user_db(form.username)
    if not form.password==user.password:
        raise HTTPException(status_code=400,detail='La contrasena no es correcta')
    
    return {'acces_token': user.username,'token_type':'bearer'} #Esta linea especifica que el token que recibe la funcion current_user es igual al nombre del usario, por eso es que se puede buscar en la base de datos, solo es bueno si practicamos en otros conextos no

@app.get('/users/me')
async def me(user:Annotated[User,Depends(current_user)]): #al poner criterios de dependencia le decimos al back que la unica form ade realizar esa opracion es primero validando que ese susario si esta registrado
    return user

#Para poder acceder a esta operacion debes de de pasarle el token(nombre de usario) en la seccion de AUth/bearer