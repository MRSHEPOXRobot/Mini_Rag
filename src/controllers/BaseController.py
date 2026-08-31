# هنا كل الملفات تقدر تورث من ال BaseController ده + إن كلهم لازم يشوفوا ال App_setting ف لازم أجيبه هنا
from helpers.config import get_settings,Settings
import os
import random
import string

class BaseController:

    def __init__(self): # Constructor Method

        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__)) # src معناه إني بقوله يرجع لل Base_dir بتاع الفولدرات
        self.file_dir = os.path.join(
            self.base_dir, # إلي هو ال Source ,Base Directory بتاعي علشان من خلاله أوصل لل file_dir
            "assets/files" # إلي موجود فيه الملفات
        )

        self.database_dir = os.path.join(
            self.base_dir,
            "assets/database"
        )

        
    def generate_random_string(self,length:int=12): # return 12_random_character
        return ''.join(random.choices(string.ascii_lowercase + string.digits,k = length) )

    def get_database_path(self,db_name:str):
        database_path = os.path.join( #full path of the database
            self.database_dir,
            db_name
        )
        if not os.path.exists(database_path): # لو مش موجودة
            os.makedirs(database_path) # إعملها
        return database_path


