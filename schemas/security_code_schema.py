from pydantic import BaseModel

class SecurityCodeRequest(BaseModel):
    telefono: str
    codigo: str
    pssw: str