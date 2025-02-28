#codigos de resouesta en HTTP
#Rangos en los codigos y their meanings
# 100-199 devuelve informacion
# 200-299 everything is ok
# 300-399 redirecciones 
# 400-499 errores de cliete
# 500-599 errores de servidor


#Codigos de HTTP con los que debmos de trabajr
# 200, 2001, 300, 3004, 400, 404 and 500

#Products

from fastapi import APIRouter
router=APIRouter(prefix='/products',#Creacion de prefijo para el router, para si no estar repituendo el mismo path y pues respetando la regla de que las peticiones siempre se hagan al mismo path
                 tags=['Productos'],
                 responses={404:{'Message':'No se ha encontrado'}}#Respuesta en caso no que no se logre lo que queramos 
                 ) 


lista_products=['Producto 1','Producto 2','Producto 3','Producto 4','Producto 5']
@router.get('/') #obtiene los recursos que tu necesitas, peticion en internet, en apis esto es mas variado!, hay otras sentencias como post=crear datos, get=obetner/leer datos, put=actualizar datos y delete=borrar
async def  usersclass(): #async=asincrono: que haga las actividades que quiera y cuando quiera 
    return lista_products

@router.get('/{id}') #obtiene los recursos que tu necesitas, peticion en internet, en apis esto es mas variado!, hay otras sentencias como post=crear datos, get=obetner/leer datos, put=actualizar datos y delete=borrar
async def  usersclass(id:int): #async=asincrono: que haga las actividades que quiera y cuando quiera 
    return lista_products[id]


