from run import app
from fastapi import APIRouter, HTTPException
from app import students_collection
from app.models import Student
from bson import ObjectId
from logs.logger import logging


router = APIRouter()
logging.info("router instance created")


logging.info("Creating API to add new student in the database")
# API to post a new student's data in the database
@router.post("/students", status_code=201)
async def create_student(student: Student):
    student_dict = student.dict()
    student_dict["address"] = student.address.dict()  

    try:
        result = students_collection.insert_one(student_dict)
        logging.info("New student successfully added into the database.\nReturning it's ID...")
        
        return {"id": str(result.inserted_id)}
    
    except Exception as e:

        logging.critical("Error occured while adding new student into the database")
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")


logging.info("Creating API to get student lists filtered by Country and Age")
# API to fetch student by ID, based on filters: country and age
@router.get("/students", status_code = 200)
async def list_students(country: str = None, age: int = None):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}

    try:
        students = list(students_collection.find(query, { "_id" : 0, "name":1 , "age":1} ))
        logging.info("Got all filtered students")

        return {"data": students}
    
    except Exception as e:

        logging.critical("Error occured while filtering students based on Country and Age")
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")


logging.info("Creating API to find student by the ID")
# API to fetch student by ID
@router.get("/students/{id}", status_code = 200 )
async def get_student(id: str):
    try:
        student = students_collection.find_one({"_id": ObjectId(id)})
        
        if student :
            
            logging.info(f"Student with the given ID {id} exists")
            
            student.pop("_id", None)
            return student
        
        else:
            
            logging.warning(f"Student with the given ID {id} doesn't exist")
            raise HTTPException(status_code=404, detail="Student not found")
        
    except Exception as e:

        logging.critical(f"Error occured while fetching student by the ID {id}")
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")


logging.info("Creating API to change student's info in the database")
# API to update student's information based on the ID
@router.patch("/students/{id}", status_code = 204)
async def update_student(id: str, student: Student):
    update_data = student.dict(exclude_unset=True)
    
    if "address" in update_data:
        update_data["address"] = student.address.dict()  # Serialize nested Address

    try:
        result = students_collection.update_one({"_id": ObjectId(id)}, 
                                                {"$set": update_data})
        logging.info("Student info patched successfully")

        if result.modified_count == 0:
            
            logging.warning(f"Student with the ID {id} doesn't exist")
            raise HTTPException(status_code=404, detail="Student not found")
        
        return {}
    except Exception as e:

        logging.critical("Error occured while patching new information")
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")


logging.info("Creating API to remove the given student from the database")
# API to delete student's data from the database based on ID
@router.delete("/students/{id}" , status_code = 200)
async def delete_student(id: str):
    try:
        result = students_collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:

            logging.warning(f"Student with ID {id} does not exist ")
            raise HTTPException(status_code=404, detail="Student not found")
        
        logging.info(f" Student with ID {id} is removed from the database")
        return {}
    
    except Exception as e:
        
        logging.critical(f"Error occured while removing student with ID {id} from the database.")
        raise HTTPException(status_code=500, detail=f"Error: {e}")


app.include_router(router)
logging.info("router instance successfully added to app instance")
