from pydantic_settings import BaseSettings,SettingsConfigDict
# فائدة ال Pydantic هي 1: تحميل القيم من ال .env
# التحقق من أنواع البيانات Validation
# تحويل البيانات للنوع المناسب Parsing 
class Settings(BaseSettings): # class settings inherts from class BaseSettings
    APP_NAME : str
    APP_VERSION : str
    OPENAI_API_KEY : str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE : int
    FILE_DEFAULT_CHUNK_SIZE : int

    class Config:
        env_file = ".env" # كل إلي في ال .env هيحصله loaded ويتحول لكلاس أقدر أستخدمه

def get_settings():
    return Settings() # return object from Settings