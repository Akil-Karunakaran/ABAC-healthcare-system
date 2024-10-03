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