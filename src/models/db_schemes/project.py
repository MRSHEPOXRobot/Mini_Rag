from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from bson.objectid import ObjectId


#Design Custom validation on schema
class Project(BaseModel):

    id: Optional[ObjectId] = Field(None,alias="_id")

    project_id: str = Field(..., min_length=1)

    @field_validator('project_id')
    @classmethod
    def validate_project_id(cls, value):#static method (cls)

        if not value.isalnum(): # isalpha_numeric
            raise ValueError('project_id must be alphanumeric')

        return value

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )


    @classmethod
    def get_indexes(cls): #static method (cls)

        return [
            {
                "key": [
                    ("project_id", 1) #ascending order
                ],
                "name": "project_id_index_1",
                "unique": True #Unique project_id
            }
        ]