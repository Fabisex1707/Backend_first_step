from fastapi import FastAPI
from Routers import users_db,jwt_auth_users
app=FastAPI()
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)
app.include_router(users_db.router_que)