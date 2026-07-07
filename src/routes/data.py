from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings,Settings
from controllers import DataController,ProjectController
import aiofiles
from models import ResponseSignal
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data", # any api will start with this prefix
    tags=  ["api_v1","data"],
) # define object

@data_router.post("/upload/{project_id}") # endpoint called upload
async def upload_data(project_id : str, file : UploadFile, # type is string,because we don't make any math operations.
                      # file is a type of UploadFile.
                      app_settings : Settings =Depends(get_settings ) ): # app_setting is an object of type settings and depends on getting settings
    data_controller = DataController()
    # validate the file properties لازم أختبر الملف إلي جايلي
    is_valid,result_signal = data_controller.validate_uploaded_file(file = file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            # ممكن لكل نوع response ترجع status_code بحيث 400 لو الدنيامش  تمام إنما 200 لو الدنيا  تمام
            content= {
                "signal":result_signal
            }
        )
    project_dir_path =  ProjectController().get_project_path(project_id=project_id)
    file_path = data_controller.generate_unique_filename(
        original_file_name = file.filename,
        project_id=project_id
    )


    try:
        async with aiofiles.open(file_path,"wb") as f: # إفتح الفايل ده كتابة بالبايناري
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e :

        logger.error(f"Error while uploading file: {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )

    return JSONResponse(
        content={
            "signal" : ResponseSignal.FILE_UPLOAD_SUCCESS.value
        }
    )

