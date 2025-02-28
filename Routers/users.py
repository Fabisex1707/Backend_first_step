#Api CRUD con una lista de datos 
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
router=APIRouter(prefix='/user',tags=['User'],responses={404:{'Error':'No se ha encontrado'}})
router_que=APIRouter()
#inicia el server: uvicorn nombre del archivo:app --reload

#Entidad user 
class User(BaseModel):#basemodel= crear una entidad pero sin el constructor usual
    #Path y Qwery
    id:int 
    name:str
    surname:str
    url:str
    age:int


users_fake_db=[
    User(id=1,name='Fabisex',surname='Castro',url='https://www.youtube.com/watch?v=0IA3ZvCkRkQ&pp=ygURaGVybyBtYXJpYWggY2FyZXk%3D',age='23'),
    User(id=2,name='Edusex',surname='Castro',url='https://www.youtube.com/watch?v=0IA3ZvCkRkQ&pp=ygURaGVybyBtYXJpYWggY2FyZXk%3D',age='23'),
    User(id=3,name='Papu',surname='Castro',url='https://www.youtube.com/watch?v=0IA3ZvCkRkQ&pp=ygURaGVybyBtYXJpYWggY2FyZXk%3D',age='23')]

#SIN ENTIDAD
@router_que.get('/usersjson') #obtiene los recursos que tu necesitas, peticion en internet, en apis esto es mas variado!, hay otras sentencias como post=crear datos, get=obetner/leer datos, put=actualizar datos y delete=borrar
async def  usersjson(): #async=asincrono: que haga las actividades que quiera y cuando quiera 
    return [
        {'Name':'Fabisex','surname':'Castro','url':'https://www.youtube.com/watch?v=0IA3ZvCkRkQ&pp=ygURaGVybyBtYXJpYWggY2FyZXk%3D','AGE':'23'},
        {'Name':'Edusex','surname':'Fack','url':'https://www.youtube.com/watch?v=0IA3ZvCkRkQ&pp=ygURaGVybyBtYXJpYWggY2FyZXk%3D','Age':'12'},
        {'Name':'Papu','surname':'Castro','url':'https://www.youtube.com/watch?v=0IA3ZvCkRkQ&pp=ygURaGVybyBtYXJpYWggY2FyZXk%3D','Age':'100'}
        ]

#CON ENTIDAD yeahhhh!
@router_que.get('/usersclass') #obtiene los recursos que tu necesitas, peticion en internet, en apis esto es mas variado!, hay otras sentencias como post=crear datos, get=obetner/leer datos, put=actualizar datos y delete=borrar
async def  usersclass(): #async=asincrono: que haga las actividades que quiera y cuando quiera 
    return users_fake_db

#get con path 
@router.get('/{id}') #uso de path al declarar que el ID ya es un parametro propio de la URL
async def  user(id:int): #async=asincrono: que haga las actividades que quiera y cuando quiera 
    return search_user(id)
    
#revisar las peticiones de get con la extension de vsCode llamado: Thunder client

#peticiones de id con query 
@router_que.get('/userquery/') #uso de query para especificar que se puedne poner otros parametros fuera del path, esto despues del /? LLave: valor 
async def  user(id:int): #async=asincrono: que haga las actividades que quiera y cuando quiera 
   return search_user(id)
    


#Uso de Post=agregar datos 
@router.post('/',status_code=201)#Codigo de cabecera si todo va bien e indicamos desde el inicio que es lo que vamos a retornar, en este caso una entidad (que definimos desde el inicio)
async def user(user:User):

    if type(search_user(user.id))==User:

        raise HTTPException(status_code=404, detail="El usario ya existe :v") #Codigo para una accion en especifico
        #Cuando lanzamos un codigo lo reflejamos con rais 
    
    else:
        users_fake_db.append(user)
        return users_fake_db


#Uso de Put=Actualizar datos, para actualizar todo el usuario
#Para put es importante enviar todos los elemntos del json, no solo un aparte, ya depende de ti que cambiar 
@router.put('/', status_code=302)
async def user(user:User):
    found=False
    for index, x in enumerate(users_fake_db):
        if x.id==user.id:
            users_fake_db[index]=user
            found=True
            return users_fake_db
    if not found:
        raise HTTPException(status_code=404,detail={"Error":"No se encontro el usario v:p"})




def search_user(id:int):
    users=filter(lambda user: user.id==id,users_fake_db)
    try:
        return list(users)[0]
    except:
        raise HTTPException(status_code=404,detail={"Error":"No se encontro el usario v:p"})
    

#Operacion para eliminar DELETE= eliminar 

@router.delete('/{id}')
async def user(id:int):
    found=False
    for index, x in enumerate(users_fake_db):

        if x.id==id:
            del users_fake_db[index]
            found=True
            return users_fake_db
    if not found:
        raise HTTPException(status_code=404,detail={"Error":"No se encontro el usario v:v"})
    
    




