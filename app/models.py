from pydantic import BaseModel
from logs.logger import logging

logging.info("Setting up Student and Address class")

class Address(BaseModel):   
    city: str
    country: str


class Student(BaseModel): 
    name: str
    age: int
    address: Address

logging.info("Student and Address class set up is complete")