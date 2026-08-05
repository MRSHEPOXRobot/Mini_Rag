# routers will be defined here and will be included in main
from fastapi import FastAPI,APIRouter,Depends # بعتمد على حاجه علشان يقدر يشتغل
import os
from helpers.config import get_settings,Settings

base_router = APIRouter(
    prefix="/api/v1", # أضف /api/v1 في بداية كل Route داخل هذا الـ Router.
    tags=  ["api_v1"], # معناها كل endpoints هتظهر في swagger تحت المجموعة api_v1.
) # define object

@base_router.get("/")
async def welcome(app_settings : Settings = Depends(get_settings ) ): #Dependency Injection
    # app_settings is a variable of class type settings and depends on function get_settings
    #app_settings = get_settings()

    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION

    return {
        "app_name":app_name,
        "app_version":app_version
    }
