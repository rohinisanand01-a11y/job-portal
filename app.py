from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "jobportal_secret_2026_secure_key_change_this_in_production"

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="amdox_db"
    )


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/options")
def options():
    return render_template("options.html")

@app.route("/jobseeker/register")
def jobseeker_register():
    return render_template("jobseekerreg.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not name or not email or not password:
        flash("All fields are required")
        return redirect(url_for("jobseeker_register"))

    hashed_password = generate_password_hash(password)

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        db.commit()
        flash("Registration successful! Please login.")
        return redirect(url_for("jobseeker_login"))

    except mysql.connector.IntegrityError:
        flash("Email already exists!")
        return redirect(url_for("jobseeker_register"))

    finally:
        cursor.close()
        db.close()

@app.route("/jobseeker/login", methods=["GET", "POST"])
def jobseeker_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Please enter email and password")
            return redirect(url_for("jobseeker_login"))

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            print(f"✅ Jobseeker logged in: ID={user['id']}, Name={user['name']}")
            return redirect(url_for("jobs"))
        else:
            flash("Invalid email or password")

    return render_template("jobseekerlogin.html")

@app.route("/employee/login", methods=["GET", "POST"])
def employee_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        if not email or not password:
            flash("Please enter email and password")
            return render_template("employeelogin.html")
        
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employers WHERE email=%s", (email,))

        employer = cursor.fetchone()
        cursor.close()
        db.close()
        
        if employer and check_password_hash(employer["password"], password):
            session["employer_id"] = employer["id"]
            session["employer_name"] = employer["name"]
            session["employer_email"] = employer["email"]
            print(f"✅ Employer logged in: ID={employer['id']}, Name={employer['name']}")
            return redirect(url_for("employer_dashboard"))
        else:
            flash("Invalid email or password")
    
    return render_template("employeelogin.html")

@app.route('/employerregister', methods=['GET', 'POST'])
def employerregister():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not name or not email or not password:
            flash('All fields are required')
            return render_template('employerregister.html')
        
        hashed_password = generate_password_hash(password)
        db = get_db_connection()
        cursor = db.cursor()

        try:
            cursor.execute("INSERT INTO employers (name, email, password) VALUES (%s, %s, %s)", 
                         (name, email, hashed_password))
            db.commit()
            print(f"✅ New employer registered: {name} (ID auto)")
            flash('Registration successful! Please login.')
            return redirect(url_for('employee_login'))
        except mysql.connector.IntegrityError:
            flash('Email already exists!')
        finally:
            cursor.close()
            db.close()
    
    return render_template('employerregister.html')


@app.route("/logout")
def logout():
    print(f"👋 Logout: {session.get('employer_name', session.get('user_name', 'User'))}")
    session.clear()
    return redirect(url_for("index"))

@app.route("/home")
def home():
    if 'user_id' not in session:
        return redirect(url_for("jobseeker_login"))
    return render_template("home.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if 'user_id' not in session:
        return redirect(url_for("jobseeker_login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    user_id = session['user_id']
    
    cursor.execute("SELECT * FROM jobseeker_profiles WHERE user_id = %s", (user_id,))
    profile = cursor.fetchone()
    
    if request.method == "POST":
        profile_data = {
            'name': request.form.get('name'),
            'dob': request.form.get('dob'),
            'gender': request.form.get('gender'),
            'email': request.form.get('email'),
            'mobile': request.form.get('mobile'),
            'address': request.form.get('address'),
            'qualification': request.form.get('qualification'),
            'institute': request.form.get('institute'),
            'pass_year': request.form.get('pass_year'),
            'experience_type': request.form.get('experience_type'),
            'total_exp': request.form.get('total_exp'),
            'company': request.form.get('company'),
            'designation': request.form.get('designation')
        }
        
        if profile:
            cursor.execute("""
                UPDATE jobseeker_profiles SET 
                name=%s, dob=%s, gender=%s, email=%s, mobile=%s, address=%s,
                qualification=%s, institute=%s, pass_year=%s, experience_type=%s,
                total_exp=%s, company=%s, designation=%s
                WHERE user_id=%s
            """, (profile_data['name'], profile_data['dob'], profile_data['gender'],
                  profile_data['email'], profile_data['mobile'], profile_data['address'],
                  profile_data['qualification'], profile_data['institute'], profile_data['pass_year'],
                  profile_data['experience_type'], profile_data['total_exp'],
                  profile_data['company'], profile_data['designation'], user_id))
            flash("✅ Profile updated successfully!")
        else:
            cursor.execute("""
                INSERT INTO jobseeker_profiles (user_id, name, dob, gender, email, mobile, address,
                                      qualification, institute, pass_year, experience_type,
                                      total_exp, company, designation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, profile_data['name'], profile_data['dob'], profile_data['gender'],
                  profile_data['email'], profile_data['mobile'], profile_data['address'],
                  profile_data['qualification'], profile_data['institute'], profile_data['pass_year'],
                  profile_data['experience_type'], profile_data['total_exp'],
                  profile_data['company'], profile_data['designation']))
            flash("✅ Profile created successfully!")
        
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for("profile"))
    
    cursor.close()
    db.close()
    return render_template("jobseekerprofile.html", profile=profile)

@app.route("/jobs")
def jobs():
    if 'user_id' not in session:
        return redirect(url_for("jobseeker_login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs ORDER BY created_at DESC")
    jobs = cursor.fetchall()

    cursor.close()
    db.close()
    return render_template("jobs.html", jobs=jobs)

@app.route("/apply/<int:job_id>", methods=["GET", "POST"])
def apply_job(job_id):
    if 'user_id' not in session:
        flash("Please login first!")
        return redirect(url_for("jobseeker_login"))

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
    job = cursor.fetchone()
    
    if not job:
        flash("Job not found!")
        return redirect(url_for('jobs'))
    
    print(f"🔍 Jobseeker {session['user_id']} viewing job {job_id} by employer {job.get('employer_id')}")
    
    if request.method == "POST":

        cursor.execute("SELECT id FROM applications WHERE user_id = %s AND job_id = %s", 
                      (session['user_id'], job_id))
        if cursor.fetchone():
            flash("You already applied for this job!")
            cursor.close()
            db.close()
            return redirect(url_for("applied_dashboard"))
        
        cursor.execute("INSERT INTO applications (user_id, job_id, status, applied_at) VALUES (%s, %s, 'pending', NOW())", 
                      (session['user_id'], job_id))
        db.commit()
        print(f"✅ APPLICATION CREATED: user_id={session['user_id']}, job_id={job_id}, employer_id={job.get('employer_id')}")
        flash("✅ Application submitted successfully!")
        
        cursor.close()
        db.close()
        return redirect(url_for("applied_dashboard"))
    
    cursor.close()
    db.close()
    return render_template("applyform.html", job=job)


@app.route("/applied_dashboard")
def applied_dashboard():
    if 'user_id' not in session:
        flash("Please login first!")
        return redirect(url_for("jobseeker_login"))
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT a.id, a.status, a.user_id, a.job_id, a.applied_at,
              j.title, j.company, j.role, j.location, j.salary 
        FROM applications a 
        JOIN jobs j ON a.job_id = j.id 
        WHERE a.user_id = %s 
        ORDER BY a.applied_at DESC
    """, (session['user_id'],))
    
    applications = cursor.fetchall()
    cursor.close()
    db.close()
    
    return render_template("applied_dashboard.html", applications=applications)


@app.route("/debug")
def debug():
    if 'employer_id' not in session:
        return "Login as employer first!"
    
    employer_id = session['employer_id']
    db = get_db_connection()
    cursor = db.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM jobs WHERE employer_id = %s", (employer_id,))
    job_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM applications", ())
    app_total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM applications a JOIN jobs j ON a.job_id = j.id WHERE j.employer_id = %s", (employer_id,))
    employer_apps = cursor.fetchone()[0]
    
    cursor.close()
    db.close()
    
    return f"""
    <h1>🔍 DEBUG INFO</h1>
    <p><strong>Employer ID:</strong> {employer_id}</p>
    <p><strong>Your Jobs:</strong> {job_count}</p>
    <p><strong>Total Applications (all):</strong> {app_total}</p>
    <p><strong>Your Applications:</strong> {employer_apps}</p>
    <a href="/employer/dashboard">← Back to Dashboard</a>
    """
@app.route("/employer/dashboard")
def employer_dashboard():
    if 'employer_id' not in session:
        print("❌ NO employer_id in session!")
        return redirect(url_for("employee_login"))
    
    employer_id = session['employer_id']
    print(f"🔍 Loading dashboard for employer_id: {employer_id}")
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM employers WHERE id = %s", (employer_id,))
    profile = cursor.fetchone()
    
    cursor.execute("SELECT * FROM jobs WHERE employer_id = %s ORDER BY created_at DESC", (employer_id,))
    jobs = cursor.fetchall()
    print(f"🔍 Found {len(jobs)} jobs for employer {employer_id}")
    cursor.execute("""
        SELECT 
            a.id, a.status, a.user_id, a.job_id, a.applied_at,
            j.title as job_title, j.company as job_company,
            COALESCE(u.name, CONCAT('User-', a.user_id)) as applicant_name,
            COALESCE(u.email, CONCAT('user', a.user_id, '@example.com')) as applicant_email
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        LEFT JOIN users u ON a.user_id = u.id
        WHERE j.employer_id = %s
        ORDER BY a.applied_at DESC
    """, (employer_id,))
    
    applications = cursor.fetchall()
    print(f"✅ FINAL RESULT: Employer {employer_id} = {len(jobs)} jobs, {len(applications)} applications")
    
    cursor.close()
    db.close()
    
    return render_template("employer_dashboard.html", 
                         profile=profile, 
                         jobs=jobs, 
                         applications=applications)

@app.route('/employer/application/<int:app_id>', methods=['GET', 'POST'])
def view_application(app_id):
    if 'employer_id' not in session:
        return redirect(url_for('employee_login'))
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            a.id, a.status, a.user_id, a.job_id, a.applied_at,
            j.title as job_title, j.company as job_company,
            COALESCE(u.name, CONCAT('User-', a.user_id)) as applicant_name,
            COALESCE(u.email, CONCAT('user', a.user_id, '@example.com')) as applicant_email,
            p.mobile as applicant_mobile
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        LEFT JOIN users u ON a.user_id = u.id
        LEFT JOIN jobseeker_profiles p ON a.user_id = p.user_id
        WHERE a.id = %s AND j.employer_id = %s
    """, (app_id, session['employer_id']))
    
    application = cursor.fetchone()
    if request.method == 'POST':
        new_status = request.form.get('status')
        cursor.execute("UPDATE applications SET status = %s WHERE id = %s", (new_status, app_id))
        db.commit()
        flash(f"✅ Status updated to '{new_status}'!")
        cursor.close()
        db.close()
        return redirect(url_for('view_application', app_id=app_id))
    
    cursor.close()
    db.close()
    
    if not application:
        flash("Application not found!")
        return redirect(url_for('employer_dashboard'))
    
    return render_template('view_applications.html', application=application)


@app.route('/employer/update-status/<int:app_id>', methods=['POST'])
def update_application_status(app_id):
    if 'employer_id' not in session:
        return redirect(url_for('employee_login'))
    
    new_status = request.form.get('status')
    db = get_db_connection()
    cursor = db.cursor()
    
    cursor.execute("""
        UPDATE applications 
        SET status = %s 
        WHERE id = %s AND job_id IN (SELECT id FROM jobs WHERE employer_id = %s)
    """, (new_status, app_id, session['employer_id']))
    
    db.commit()
    cursor.close()
    db.close()
    
    flash(f"✅ Status updated to '{new_status}'!")
    return redirect(url_for('employer_dashboard'))

@app.route('/employer/applicant/<int:user_id>')
def employer_view_applicant(user_id):
    if 'employer_id' not in session:
        return redirect(url_for('employee_login'))
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
    applicant = cursor.fetchone()
    
    cursor.execute("""
        SELECT * FROM jobseeker_profiles 
        WHERE user_id = %s
    """, (user_id,))
    detailed_profile = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    if not applicant:
        flash("Applicant not found!")
        return redirect(url_for('employer_dashboard'))
    
    return render_template('applicant_profile.html', 
                         applicant=applicant, 
                         detailed_profile=detailed_profile)


@app.route('/employer/profile', methods=['GET', 'POST'])
def employer_profile():
    if 'employer_id' not in session:
        return redirect(url_for('employee_login'))
    
    employer_id = session['employer_id']
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form.get('mobile', '')
        city = request.form.get('city', '')
        
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE employers 
            SET name=%s, email=%s, mobile=%s, city=%s 
            WHERE id=%s
        """, (name, email, mobile, city, employer_id))
        db.commit()
        cursor.close()
        db.close()
        
        flash('✅ Profile updated successfully!')
        return redirect(url_for('employer_dashboard'))
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employers WHERE id = %s", (employer_id,))
    profile = cursor.fetchone()
    cursor.close()
    db.close()
    
    return render_template('employer_profile.html', profile=profile)

@app.route('/employer/post-job', methods=['GET', 'POST'])
def post_job():
    if 'employer_id' not in session:
        return redirect(url_for('employee_login'))
    
    if request.method == 'POST':
        title = request.form.get('title', '')
        role = request.form.get('role', '')
        company = request.form.get('company', '')
        location = request.form.get('location', '')
        salary = request.form.get('salary', '')
        description = request.form.get('description', '')
        
        final_title = title or role
        
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO jobs (title, company, location, salary, description, employer_id, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """, (final_title, company, location, salary, description, session['employer_id']))
        job_id = cursor.lastrowid
        db.commit()
        print(f"✅ JOB CREATED: ID={job_id}, employer_id={session['employer_id']}, title='{final_title}'")
        cursor.close()
        db.close()
        
        flash('✅ Job posted successfully!')
        return redirect(url_for('employer_dashboard'))
    
    return render_template('post_job.html')

if __name__ == "__main__":
    app.run(debug=True)
