from pymongo import MongoClient
import bcrypt
from bson.objectid import ObjectId

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['medicalapp']  # Database

# Hash password using bcrypt
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Insert Doctors
doctors = [
    {
        "_id": ObjectId(),  # MongoDB generates a unique _id if not specified
        "name": "Dr. John Doe",
        "email": "john.doe@example.com",
        "password": hash_password("password123"),  # Hash password before inserting
        "role": "doctor"
    },
    {
        "_id": ObjectId(),
        "name": "Dr. Jane Smith",
        "email": "jane.smith@example.com",
        "password": hash_password("password456"),
        "role": "doctor"
    }
]

# Insert Patients
patients = [
    {
        "_id": ObjectId(),
        "name": "Patient A",
        "email": "patient.a@example.com",
        "password": hash_password("patientpassword1"),
        "role": "patient",
        "doctor_id": doctors[0]["_id"],  # Associate with Dr. John Doe
        "prescription": None
    },
    {
        "_id": ObjectId(),
        "name": "Patient B",
        "email": "patient.b@example.com",
        "password": hash_password("patientpassword2"),
        "role": "patient",
        "doctor_id": doctors[1]["_id"],  # Associate with Dr. Jane Smith
        "prescription": None
    }
]

# Insert doctors into 'users' collection
db.users.insert_many(doctors)
print("Doctors inserted successfully")

# Insert patients into 'patients' collection
db.patients.insert_many(patients)
print("Patients inserted successfully")
