from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from cryptography.fernet import Fernet
import bcrypt
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/medicalapp'

# MongoDB Setup
mongo = PyMongo(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Generate encryption key for prescriptions
fernet_key = Fernet.generate_key()
cipher_suite = Fernet(fernet_key)

# Load user for login session
@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data['_id'], user_data['role'])
    return None

class User(UserMixin):
    def __init__(self, user_id, role):
        self.id = str(user_id)
        self.role = role

@app.route('/')
def index():
    return render_template('login.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        if role=="doctor":
            user = mongo.db.users.find_one({"email": email})

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                user_obj = User(user['_id'], user['role'])
                login_user(user_obj)
                if user['role'] == 'doctor':
                    return redirect(url_for('doctor_dashboard'))
        else:
            user = mongo.db.patients.find_one({"email": email})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            user_obj = User(user['_id'], user['role'])
            print("fs",user_obj)
            if user['role'] == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            else:
                session['username']=email
                return redirect(url_for('patient_dashboard'))
        
        else:
            flash('Invalid email or password.')
    return render_template('login.html')

@app.route('/login1', methods=['GET', 'POST'])
def login1():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = mongo.db.patients.find_one({"email": email})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            user_obj = User(user['_id'], user['role'])
            print("fs",user_obj)
            if user['role'] == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            else:
                session['username']=email
                return redirect(url_for('patient_dashboard'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html')

# Doctor's Dashboard
@app.route('/doctor', methods=['GET'])
@login_required
def doctor_dashboard():
    if current_user.role == 'doctor':
        patients = mongo.db.patients.find({"doctor_id": ObjectId(current_user.id)})
        return render_template('doctor.html', patients=patients)
    return redirect(url_for('login'))

# View Patient Info and Write Prescription
@app.route('/doctor/patient/<patient_id>', methods=['GET', 'POST'])
@login_required
def view_patient(patient_id):
    if current_user.role == 'doctor':
        patient = mongo.db.patients.find_one({"_id": ObjectId(patient_id), "doctor_id": ObjectId(current_user.id)})
        if request.method == 'POST':
            prescription = request.form['prescription']
            encrypted_prescription = cipher_suite.encrypt(prescription.encode())
            mongo.db.patients.update_one(
                {"_id": ObjectId(patient_id)},
                {"$set": {"prescription": encrypted_prescription}}
            )
            return redirect(url_for('doctor_dashboard'))
        return render_template('view_patient.html', patient=patient)
    return redirect(url_for('login'))

# Patient's Dashboard
# Patient's Dashboard
@app.route('/patient', methods=['GET'])
@login_required
def patient_dashboard():
    # Use find_one to get a single document
    patient = mongo.db.patients.find_one({"email": session["username"]})
    if patient:  # Check if the patient exists
        if patient.get('prescription'):
            decrypted_prescription = cipher_suite.decrypt(patient['prescription']).decode()
        else:
            decrypted_prescription = None
        # Fetch patient details
        name = patient.get('name', 'N/A')
        age = patient.get('age', 'N/A')
        address = patient.get('address', 'N/A')
        phone_number = patient.get('phone_number', 'N/A')
        
        return render_template('patient.html', patient=patient, prescription=decrypted_prescription, name=name,age=age, address=address, phone_number=phone_number)
    
    return redirect(url_for('login'))



# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)