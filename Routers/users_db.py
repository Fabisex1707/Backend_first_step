#Api CRUD con MongoDB
from fastapi import APIRouter, HTTPException, status
from  bd.models.user import User #Entidad user 
from bd.client import db_cliente
from bd.schemas.user import user_schema, users_schema
from bson import ObjectId
router=APIRouter(prefix='/usersdb',tags=['userdb'],responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}})
router_que=APIRouter(prefix='/usersdbs')
#inicia el server: uvicorn nombre del archivo:app --reload

users_fake_db=[]

#CON ENTIDAD yeahhhh!
@router_que.get('/',response_model=list[User]) #obtiene los recursos que tu necesitas, peticion en internet, en apis esto es mas variado!, hay otras sentencias como post=crear datos, get=obetner/leer datos, put=actualizar datos y delete=borrar
async def  usersclass(): #async=asincrono: que haga las actividades que quiera y cuando quiera 
    return users_schema(db_cliente.users.find())

#get con path 
@router.get('/{id}') #uso de path al declarar que el ID ya es un parametro propio de la URL
async def  user(id:str): #async=asincrono: que haga las actividades que quiera y cuando quiera 
    return search_user("_id",ObjectId(id))

#peticiones de id con query 
@router_que.get('/userquery/') #uso de query para especificar que se puedne poner otros parametros fuera del path, esto despues del /? LLave: valor 
async def  user(id:str): #async=asincrono: que haga las actividades que quiera y cuando quiera 
   return search_user("_id",ObjectId(id))
    


#Uso de Post=agregar datos 
@router.post('/',response_model=User,status_code=status.HTTP_201_CREATED)#Codigo de cabecera si todo va bien e indicamos desde el inicio que es lo que vamos a retornar, en este caso una entidad (que definimos desde el inicio)
async def user(user:User):
    if type(search_user_by_email(user.email))==User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El email ya esta registrado :v") #Codigo para una accion en especifico
        #Cuando lanzamos un codigo lo reflejamos con rais 
    
    user_dict=dict(user)
    del user_dict["id"]
    id=db_cliente.users.insert_one(user_dict).inserted_id #Esto no se autocompleta pq estamos creandolo desde cero, el lugar donde estamos trabajando (Local) y el nombre del esquema
    
    new_user=user_schema(db_cliente.users.find_one({"_id":id}))
    #El nombre de la clave unica que crea fastAPI es "_id"
    #si bien aqui estamos pidiendo que se nos devuelvan los datos del id que insertamos en la linea 41
    #Estos no vienen con el meodelos/esquema que necesitamos, po lo que creamos un nuevo modelo/esquema
    #en user.py\schemas, esto para resolver el problema. 
    return User(**new_user)

#Uso de Put=Actualizar datos, para actualizar todo el usuario
#Para put es importante enviar todos los elemntos del json, no solo un aparte, ya depende de ti que cambiar 
@router.put('/',response_model=User,status_code=status.HTTP_302_FOUND)
async def user(user:User):

    dict_user=dict(user)
    del dict_user["id"]
    try:
        correo_repetido=db_cliente.users.find_one({"email": user.email, "_id": {"$ne": ObjectId(user.id)}}) #"$ne" es la forma not en mongodb
        if correo_repetido:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"El email ya esta registrado en otro usario:v"})
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"Error":"No se encontro el usario o el email ya esta registrado en otro usario:"})
    try:
        db_cliente.users.find_one_and_replace({"_id":ObjectId(user.id)},dict_user)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"Error":"No se encontro el usario v:v"})
    return search_user("_id",ObjectId(user.id))

def search_user_by_email(email:str):
    try:
        user=db_cliente.users.find_one({"email":email})
        return User(**user_schema(user))
    except:
        return {"Error":"No se encontro el usario v:p"}
  
##### Otro momento######
def search_user(field:str,value):
    try:
        user=db_cliente.users.find_one({field:value})#Busamos dentro de la bd un campo x y un valor y
        return User(**user_schema(user))
    except:
        return {"Error":"No se encontro el usario v:p"}

    

#Operacion para eliminar DELETE= eliminar 

@router.delete('/{id}')
async def user(id:str):
    found=db_cliente.users.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"Error":"No se encontro el usario v:v"})
    

    
