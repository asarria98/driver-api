from pydantic import BaseModel, HttpUrl
from datetime import date
from typing import Optional

class Driver(BaseModel):
    driverId: int
    driverRef: str
    number: Optional[int]  # Puede ser opcional si algunos no tienen número
    code: Optional[str]
    forename: str
    surname: str
    dob: date  # Tipo de dato fecha
    nationality: str
    url: HttpUrl  # Para validar que es una URL válida
