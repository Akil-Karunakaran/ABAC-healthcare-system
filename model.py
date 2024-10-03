from flask_login import UserMixin

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, role):
        self.id = str(user_id)  # The user ID needs to be a string
        self.role = role

    def is_authenticated(self):
        return True  # You can adjust logic based on your needs

    def is_active(self):
        return True  # Can also be customized to check if user is active

    def is_anonymous(self):
        return False  # The user is not anonymous

    def get_id(self):
        return self.id  # Flask-Login needs this method

class Patient:
    def __init__(self, patient_id, doctor_id, name, prescription):
        self.id = patient_id
        self.doctor_id = doctor_id
        self.name = name
        self.prescription = prescription
