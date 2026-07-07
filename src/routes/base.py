# routers will be defined here and will be included in main
from fastapi import FastAPI,APIRouter,Depends # بعتمد على علشان أقدر أشتغل
import os
from helpers.config import get_settings,Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=  ["api_v1"],
) # define object

@base_router.get("/")
async def welcome(app_settings : Settings =Depends(get_settings ) ):
    # app_settings is an object of class type settings and depends on function get_settings
    #app_settings = get_settings()

    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION

    return {
        "app_name":app_name,
        "app_version":app_version
    }
