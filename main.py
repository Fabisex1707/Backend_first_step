from fastapi import FastAPI
from Routers import codes_routers, users
from fastapi.staticfiles import StaticFiles
app=FastAPI()


app.include_router(codes_routers.router)
app.include_router(users.router)
app.include_router(users.router_que)
#mostrar recurosos estaticos 
app.mount('/statics', StaticFiles(directory='statics'), name='static')#en la parte de directory='Debo de poner le nombre de la carpeta donde guardo todo'
app.mount('/staticos', StaticFiles(directory='statics'), name='static')#con un solo diectorio puedes ver todas los recursos, solo cambia de carpeta si quieres mostarar otras cosas

@app.get('/') #obtiene los recursos que tu necesitas, peticion en internet, en apis esto es mas variado!
async def  root(): #async=asincrono: que haga las actividades que quiera y cuando quiera 
    return '!Hola fastAPI!'



@app.get('/url_fabisexx') #obtiene los recursos que tu necesitas
async def  url(): #async=asincrono: que haga las actividades que quiera y cuando quiera 
    return {'URL':'https://mouredev.com/python'}

#inicia el server: uvicorn nombre del archivo:app --reload
#Detener el server Ctrl + C
# Documentacion con Swagger: http://127.0.0.1:8000/docs
# Documnetacion con Redocly: http://127.0.0.1:8000/redoc
# A lo largo de este curso hemos creado 3 apis basicas, ahora necesitamos que estas se conecten entre si para hacer mas facil su uso 
#Es por ello que usaremos Routers







