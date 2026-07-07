from fastapi import FastAPI
from routes import base,data
from controllers import DataController,ProjectController,BaseController
app = FastAPI() # app is object from function called FastAPI

app.include_router(base.base_router)
app.include_router(data.data_router)