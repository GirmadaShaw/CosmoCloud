from fastapi import FastAPI
from logs.logger import logging

app = FastAPI()  # creating FastAPI instance
logging.info("FastAPI instance created successfully")


from app.router import router
 
