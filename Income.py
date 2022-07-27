from pydantic import BaseModel

class Income(BaseModel):
    age: int
    workclass: str
    education: str
    maritalstatus: str
    occupation: str
    relationship: str
    race: str
    gender: str
    capitalgain: int
    capitalloss: int
    hoursperweek: int
    nativecountry: str
