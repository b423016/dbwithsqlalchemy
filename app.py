# the mainfel that ahndels the http requests & starts the sever
# need to add the cors 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # cross resource origin sharing
from backend.api import routes
from backend.database import db_engine, models # to interact with db
from backend.middleware.cors_middleware import setup_cors 

#to create the db tabble which is equivalent to the migration 
models.Base.metadata.create_all(bind=db_engine.engine)
# this is okay for a small project but for larger ones we need alembic

#fastapi instance
app = FastAPI(
    title="db fucker",
    description="managing the user in the db syss",
    version="0.0.1",
    contact={"name": "Ayush Jha", "email": "billupajji069@gmail.com",},
)
# Set up CORS middleware
setup_cors(app) 

app.include_router(routes.router) # to include the api routers from the routes module
# the api in routes module is included in the app
@app.get("/")
def read_root(): # root end
    return {"message": "Welcome to the db fucker"}

