from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
ALGORITHM="HS256" #Este numero lo saque de la pagina jwt debugger: https://jwt.io 
acces_token_duration_minute=30 #Establecemos el tiempo en el que el token sera valido 1min
SECRET="57eaf25cee2d3a4f00e8cac2c284a144327d17699014d9bbff04f1ca44bfca0e" #Esto se genera a traves del comando "openssl rand -hex 32"
crypt= CryptContext(schemes=["bcrypt"])

router=APIRouter()
outh2= OAuth2PasswordBearer(tokenUrl='login')

#Entidades
class User(BaseModel):#basemodel= crear una entidad pero sin el constructor usual
    #Path y Qwery
    username:str|None=None
    full_name:str
    email:str
    disabled:bool
#apliacion de la herencia en poo
class user_db(User):
    password:str |None=None
    token_version:int |None=None



#En principio os datos se ven asi pues solo es un ajemplo, pero a futuro hay que usar un "hash"
#Base de datos falsa
users_db={
    'Fabian':{
        'username':"Fabian",
        'full_name':'Fabian Castro Dolores',
        'email':'Camikami1707@xd.com',
        'disabled':False,
        'password':'$2a$12$ghYKAQQslQxTUIt3gAs76eLRNnfULkYNUZUlbapB09wMKDV3EYX0O',
        'token_version': 0
    },
    'Fabi_2':{
        'username':"Fabi_2",
        'full_name':'Fabian Castro D',
        'email':'Camikami1707@xd.com',
        'disabled':True,
        'password':'$2a$12$ghYKAQQslQxTUIt3gAs76eLRNnfULkYNUZUlbapB09wMKDV3EYX0O',
        'token_version': 0
    },
    'Violeta':{
        'username':"Violeta",
        'full_name':'Fabian Castro D',
        'email':'Camikami1707@xd.com',
        'disabled':False,
        'password':'$2a$12$tm.gmjPb1gSdW/loLDxb/O8Ttl7rSt3AfE13RlivhmGBG9s/Q/.Pa',
        'token_version': 0
    }
}
#Funciones
def search_user_db(username:str):
    if username in users_db:
        return user_db(**users_db[username])
    
def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token:Annotated[str, Depends(outh2)]):
    exception=HTTPException(status_code=401,
                      detail='Credenciales invalidas',
                      headers={'www-Authenticte':' bearer'})
    try:
        payl= jwt.decode(token,SECRET,algorithms=[ALGORITHM])
        username=payl.get("sub")
        if username is None:
            raise exception
        
        user = search_user(username)
        if user is None:
            raise exception
    except JWTError:
        raise exception
    
    return user

async def auth_user_db(token:Annotated[str, Depends(outh2)]):
    exception=HTTPException(status_code=401,
                      detail='Credenciales invalidas',
                      headers={'www-Authenticte':' bearer'})
    try:
        payl= jwt.decode(token,SECRET,algorithms=[ALGORITHM])
        username=payl.get("sub")
        token_version=payl.get("token_version")
        if username is None:
            raise exception
        
        user = search_user_db(username)
        if user is None:
            raise exception
        
        if token_version != user.token_version:
            raise HTTPException(status_code=401, detail="Token inválido o desactualizado")
    except JWTError:
        raise exception
    
    return user

async def current_user(user:Annotated[User,Depends(auth_user)]):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                      detail='Usario inactivo')
    
    return user


def current_user_db(user:Annotated[user_db,Depends(auth_user_db)]):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                      detail='Usario inactivo')
    return user

   

#Operacion get
@router.post('/login')
async def login(form:Annotated[OAuth2PasswordRequestForm,Depends()]):
    userdb=users_db.get(form.username)

    if not userdb:
        raise HTTPException(status_code=400,detail='El usario no es correcto')
    
    user=search_user_db(form.username)
    if not crypt.verify(form.password,user.password):
        raise HTTPException(status_code=400,detail='La contrasena no es correcta')
    
    
    #acces_token_expiration=timedelta(minutes=acces_token_duration) #aqui le decimos la diferencia de tiempo que queremos que pase para que expire el token 
    
    #expire=datetime.now(timezone.utc) + timedelta(minutes=acces_token_duration) Eliminamos estas variables pq podemos poner todo esto en el lugar que lo necesitemos

    acces_token={"sub":user.username, 
                 "exp":datetime.now(timezone.utc) + timedelta(minutes=acces_token_duration_minute),
                 "token_version":user.token_version
                 }
    
    return {'acces_token': jwt.encode(acces_token,SECRET,algorithm=ALGORITHM),'token_type':'bearer'} 
                        #  aqui estamos encriptando la informacion que nos devuelve el login, en este caso un Json con datos como: 
                        # username 
                        # fecha de expiracion 
                        # tipo de token que envia 
                        # la llave para dar permiso 

@router.get('/users/me')
async def me(user:Annotated[User,Depends(current_user)]): #al poner criterios de dependencia le decimos al back que la unica form ade realizar esa opracion es primero validando que ese susario si esta registrado
    return user


'''''
Esto es lo que devuelve la operacion de login, es un Json mucho mas comlejo, pero esto no es un token y no sirve para que queremos :v
{
  "acces_token": {
    "sub": "Fabisex",
    "exp": "2025-01-04T04:35:17.714561+00:00"
  },
  "token_type": "bearer"
}
'''''


@router.post('/register')
async def register(user: user_db):
    if user.username in users_db:
        raise HTTPException(
            status_code=400,
            detail='El usuario ya está registrado'
        )
    users_db[user.username] = {
    "username": user.username,
    "full_name": user.full_name,
    "email": user.email,
    "disabled": user.disabled,
    "password": crypt.hash(user.password),
    'token_version': 0

    }
    return users_db

@router.put('/update',status_code=status.HTTP_200_OK)
async def update(token: Annotated[str, Depends(outh2)],user_update: user_db):
    exception=HTTPException(status_code=401,
                      detail='Credenciales invalidas',
                      headers={'www-Authenticte':' bearer'})
    try:
        payl= jwt.decode(token,SECRET,algorithms=[ALGORITHM])
        username=payl.get("sub")
        token_version=payl.get("token_version")
        if username is None:
            raise exception
        
        stored_user = users_db.get(username)

        user = search_user(username)
        if user is None:
            raise exception
        
        if token_version != stored_user['token_version']:
            raise HTTPException(status_code=401, detail="Token desactualizado o inválido")
    except JWTError:
        raise exception

   
    if not stored_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    

    stored_user.update({
        "full_name": user_update.full_name,
        "email": user_update.email,
        "disabled": user_update.disabled,
        "password": crypt.hash(user_update.password) if user_update.password else stored_user["password"],
        "token_version": stored_user["token_version"] + 1  # Incrementar token_version
    })
    users_db[username] = stored_user
    
    return stored_user

@router.delete('/borrar',status_code=status.HTTP_200_OK)
async def vanish(token: Annotated[str, Depends(outh2)]):
    exception=HTTPException(status_code=401,
                      detail='Credenciales invalidas',
                      headers={'www-Authenticte':' bearer'})
    try:
        payl= jwt.decode(token,SECRET,algorithms=[ALGORITHM])
        username=payl.get("sub")
        
        if username is None:
            raise exception
        
        user = search_user_db(username)
        if user is None:
            raise exception
        
    except JWTError:
        raise exception
    found=False
    for x in users_db:
        if x == username:
            del (users_db[username])
            found=True
            return users_db
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No se encontro el usario')
    
# Pendientes: 
# revisar la relacion del token de auth_user y auth_user_db
# problema al actualizar, creo que no se actualiza porque no tiene un token valido, ya que usamos auth_user_db y este no genera un token propio
# Los datos de user_db no se actualizan debido a que las funciones que desencriptan los datos del token, solo retornan datos del usario y eso tiene influencia en los datos
# #
# Soluciones: 
# dejar de usar current_user_db y auth_user_db, ya que cada uno solo nos devolvia los datos de un usario, cosa que relacionabamos con user(la varaible que usaria la clase User y serian los espacios que rellenariamos con el json) y lo que ocacionaba que no se pudieran actalizar lo datos
# usamos directamnete la variable outh2, ya que contenia el token que tenia el nombre del usario y la version del token que usaba, asi solo para hacer los cambios en el usario que tenia el toekn de iniico de sesion y cambiar la version para que caduque y tenga que hacer login de nuevo
# 
# # 