from pydantic import BaseModel,Field
class User(BaseModel):#basemodel= crear una entidad pero sin el constructor usual
    #Path y Qwery
    id: str | None = Field(default=None, description="MongoDB ObjectID")
    username: str = Field(..., description="User name", max_length=50)
    email: str = Field(..., description="Email Valid")