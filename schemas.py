from pydantic import BaseModel

class ContactSchema(BaseModel):
    email: str
    firstname: str
    lastname: str
    phone: str
    website: str