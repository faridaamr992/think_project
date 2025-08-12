from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        # validator function to accept ObjectId or valid str
        def validate(value, _info):
            if isinstance(value, ObjectId):
                return value
            if isinstance(value, str) and ObjectId.is_valid(value):
                return ObjectId(value)
            raise ValueError("Invalid ObjectId")

        # schema says: input is str, output validated by `validate`
        return core_schema.general_after_validator_function(
            validate,
            core_schema.str_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema):
        return {
            "type": "string",
            "pattern": "^[a-fA-F0-9]{24}$",
            "title": "ObjectId",
            "examples": ["507f1f77bcf86cd799439011"],
        }

class UserSchema(BaseModel):
    id: PyObjectId = Field(alias="_id")
    username: str
    email: str

    model_config = {
        "populate_by_name": True,
        "json_encoders": {ObjectId: str},
    }
