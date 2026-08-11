from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    #Every Record in chunks should have these fields.
    _id: Optional[ObjectId] = Field(None,alias="_id")

    chunk_text: str = Field(...,min_length=1)
    chunk_metadata: dict

    chunk_order: int = Field(...,gt=0) #Should be greater than 0.
    chunk_project_id: ObjectId


    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )