from pymongo import MongoClient
#Base de datos local
#db_cliente=MongoClient().local#Entre estos parentisis hay que poner la URL de la base de datos que nos queremos conectar, en este caos no lo ponemos pq nos queremos conectar al localhost

db_cliente=MongoClient("mongodb+srv://fabiancastrod:GXJm4FYKMrLQleWU@cluster0.mdalh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").usersfab 
                                                                                                                                                #Este nombre es el que yo quiera, que puede venir uno de cabecera pues no hay problema


