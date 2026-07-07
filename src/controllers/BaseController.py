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
def generate_random_string(self,length:int=12):
    return ' '.join(random.choices(string.ascii_lowercase + string.digits,k = length) )