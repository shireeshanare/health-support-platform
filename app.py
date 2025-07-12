from flask import Flask, request, redirect, url_for, session, render_template_string
from pymongo import MongoClient
import pandas as pd

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MongoDB Connection Setup
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client['health_support_platform']  # Database name
users_collection = db['users']  # Collection for users
diseases_collection = db['diseases']  # Collection for diseases (you can later store symptom data here)

# Load disease data into MongoDB if not already present (only once)
def initialize_diseases():
    if diseases_collection.count_documents({}) == 0:
        disease_data = [
            {"disease": "Flu", "symptoms": ["Fever", "Cough", "Fatigue"], "treatment": "Rest, Hydration, Antiviral Medication"},
            {"disease": "Diabetes", "symptoms": ["Increased Thirst", "Fatigue", "Blurry Vision"], "treatment": "Insulin, Exercise, Healthy Diet"},
            {"disease": "Hypertension", "symptoms": ["Headache", "Dizziness", "Chest Pain"], "treatment": "Lifestyle Changes, Medication"}
        ]
        diseases_collection.insert_many(disease_data)

initialize_diseases()

# Dummy users database stored in MongoDB
def find_user_by_username(username):
    return users_collection.find_one({"username": username})

# Home Page (with Register, Login, About Us, Symptom Checker, and Chatbot)
@app.route('/')
def home():
    if 'username' in session:
        return render_template_string(''' 
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Home</title>
            <style>
                body {
                    text-align: center;
                    background-image: url('https://wallpaperaccess.com/full/136949.jpg');
                    background-size: cover;
                    background-position: center;
                    height: 100vh;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    color: white;
                }
                .container {
                    background-color: rgba(0, 0, 0, 0.7);
                    padding: 20px;
                    border-radius: 10px;
                }
                a {
                    display: block;
                    color: white;
                    margin: 10px;
                    text-decoration: none;
                    font-size: 20px;
                    padding: 10px;
                    border: 2px solid white;
                    border-radius: 5px;
                }
                a:hover {
                    background-color: white;
                    color: black;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to the Health Support Platform</h1>
                <a href="/symptom_checker">Symptom Checker</a>
                <a href="/chatbot">Mental Health Chatbot</a>
                <a href="/logout">Logout</a>
                <a href="/about_us">About Us</a>
            </div>
        </body>
        </html>
        ''')
    else:
        return render_template_string(''' 
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Home</title>
            <style>
                body {
                    text-align: center;
                    background-image: url('https://wallpaperaccess.com/full/136949.jpg');
                    background-size: cover;
                    background-position: center;
                    height: 100vh;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    color: white;
                }
                .container {
                    background-color: rgba(0, 0, 0, 0.7);
                    padding: 20px;
                    border-radius: 10px;
                }
                a {
                    display: block;
                    color: white;
                    margin: 10px;
                    text-decoration: none;
                    font-size: 20px;
                    padding: 10px;
                    border: 2px solid white;
                    border-radius: 5px;
                }
                a:hover {
                    background-color: white;
                    color: black;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Health Support Platform</h1>
                <a href="/register">Register</a>
                <a href="/login">Login</a>
                <a href="/about_us">About Us</a>
            </div>
        </body>
        </html>
        ''')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        # Check if username exists in MongoDB
        if users_collection.find_one({"username": username}):
            return render_template_string('''
            <h2>Username already exists. Please try a different one.</h2>
            ''')
        
        # Insert new user into MongoDB
        users_collection.insert_one({
            "full_name": full_name,
            "email": email,
            "username": username,
            "password": password
        })
        return redirect(url_for('registration_successful'))

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Register</title>
        <style>
            body {
                text-align: center;
                background-image: url('https://wallpaperaccess.com/full/1917331.jpg');
                background-size: cover;
                background-position: center;
                height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: white;
            }
            .container {
                background-color: rgba(0, 0, 0, 0.7);
                padding: 40px;
                border-radius: 10px;
                width: 40%;
                border: 2px solid white;
            }
            input, button {
                margin: 10px;
                padding: 10px;
                width: 100%;
                border: 2px solid white;
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.8);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Register</h2>
            <form method="post">
                <input type="text" name="full_name" placeholder="Full Name" required><br>
                <input type="email" name="email" placeholder="Email" required><br>
                <input type="text" name="username" placeholder="Username" required><br>
                <input type="password" name="password" placeholder="Password" required><br>
                <button type="submit">Register</button>
            </form>
        </div>
    </body>
    </html>
    ''')

# Registration Successful Page
@app.route('/registration_successful')
def registration_successful():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Registration Successful</title>
        <style>
            body {
                text-align: center;
                background-image: url('https://wallpaperaccess.com/full/1917331.jpg');
                background-size: cover;
                background-position: center;
                height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: white;
            }
            .container {
                background-color: rgba(0, 0, 0, 0.7);
                padding: 40px;
                border-radius: 10px;
                width: 40%;
                border: 2px solid white;
            }
            a {
                color: white;
                text-decoration: none;
                font-size: 18px;
                border: 1px solid white;
                padding: 10px;
                border-radius: 5px;
            }
            a:hover {
                background-color: white;
                color: black;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Registration Successful!</h2>
            <a href="/">Return to Home</a>
        </div>
    </body>
    </html>
    ''')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials in MongoDB
        user = find_user_by_username(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect('/')
        else:
            return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Invalid Login</title>
                <style>
                    body {
                        text-align: center;
                        background-image: url('https://wallpaperaccess.com/full/749802.jpg');
                        background-size: cover;
                        background-position: center;
                        height: 100vh;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        color: white;
                    }
                    .container {
                        background-color: rgba(0, 0, 0, 0.7);
                        padding: 40px;
                        border-radius: 10px;
                        width: 40%;
                        border: 2px solid white;
                    }
                    input, button {
                        margin: 10px;
                        padding: 10px;
                        width: 100%;
                        border: 2px solid white;
                        border-radius: 5px;
                        background-color: rgba(255, 255, 255, 0.8);
                    }
                    .error-message {
                        color: red;
                        font-size: 18px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Invalid Username or Password</h2>
                    <p class="error-message">Please check your login details and try again.</p>
                    <a href="/login">Go back to Login</a>
                </div>
            </body>
            </html>
            ''')

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
        <style>
            body {
                text-align: center;
                background-image: url('https://wallpaperaccess.com/full/749802.jpg');
                background-size: cover;
                background-position: center;
                height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: white;
            }
            .container {
                background-color: rgba(0, 0, 0, 0.7);
                padding: 40px;
                border-radius: 10px;
                width: 40%;
                border: 2px solid white;
            }
            input, button {
                margin: 10px;
                padding: 10px;
                width: 100%;
                border: 2px solid white;
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.8);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Login</h2>
            <form method="post">
                <input type="text" name="username" placeholder="Username" required><br>
                <input type="password" name="password" placeholder="Password" required><br>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    ''')

# Symptom Checker Page
@app.route('/symptom_checker', methods=['GET', 'POST'])
def symptom_checker():
    if request.method == 'POST':
        symptoms_input = request.form['symptoms']
        symptoms_list = symptoms_input.lower().split(',')

        # Find matching diseases from MongoDB
        matching_diseases = []
        for disease in diseases_collection.find():
            disease_name = disease['disease']
            disease_symptoms = [symptom.lower() for symptom in disease['symptoms']]
            if any(symptom in disease_symptoms for symptom in symptoms_list):
                matching_diseases.append(disease_name)

        if matching_diseases:
            return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Symptom Checker Results</title>
                <style>
                    body {
                        text-align: center;
                        background-image: url('https://wallpaperaccess.com/full/749802.jpg');
                        padding: 50px;
                    }
                    .result {
                        background-color: #ffffff;
                        padding: 20px;
                        margin: 10px;
                        border-radius: 10px;
                        border: 1px solid #ccc;
                    }
                </style>
            </head>
            <body>
                <h1>Possible Diseases based on your Symptoms</h1>
                <div class="result">
                    <h3>Matching Diseases:</h3>
                    <ul>
                        {% for disease in matching_diseases %}
                            <li>{{ disease }}</li>
                        {% endfor %}
                    </ul>
                    <a href="/">Return to Home</a>
                </div>
            </body>
            </html>
            ''', matching_diseases=matching_diseases)

        return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>No Matching Diseases</title>
            <style>
                body {
                    text-align: center;
                    background-image: url('https://wallpaperaccess.com/full/1076735.jpg');
                    padding: 50px;
                }
                .result {
                    background-color: #ffffff;
                    padding: 20px;
                    margin: 10px;
                    border-radius: 10px;
                    border: 1px solid #ccc;
                }
            </style>
        </head>
        <body>
            <h1>No Matching Diseases Found</h1>
            <p>It seems like we couldn't find a match for your symptoms. Please consult a doctor for further assistance.</p>
            <a href="/">Return to Home</a>
        </body>
        </html>
        ''')

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Symptom Checker</title>
        <style>
            body {
                text-align: center;
                background-image: url('https://wallpaperaccess.com/full/1551132.jpg');
                padding: 50px;
            }
            .form-container {
                background-color: #ffffff;
                padding: 20px;
                margin: 10px;
                border-radius: 10px;
                border: 1px solid #ccc;
                width: 60%;
                margin: auto;
            }
            input, button {
                padding: 10px;
                margin: 10px;
                width: 100%;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            button {
                background-color: #4CAF50;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>Enter your Symptoms</h2>
            <form method="post">
                <input type="text" name="symptoms" placeholder="Enter symptoms separated by commas" required><br>
                <button type="submit">Check Symptoms</button>
            </form>
        </div>
    </body>
    </html>
    ''')

# About Us Page
@app.route('/about_us')
def about_us():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>About Us</title>
        <style>
            body {
                text-align: center;
                background-image: url('https://wallpaperaccess.com/full/1551132.jpg');
                padding: 50px;
            }
            .container {
                background-color: #ffffff;
                padding: 20px;
                margin: 10px;
                border-radius: 10px;
                border: 1px solid #ccc;
                width: 60%;
                margin: auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>About Us</h1>
            <p>We are a team of healthcare professionals and developers committed to providing support for your health. Our platform aims to offer easy access to healthcare solutions.</p>
            <a href="/">Return to Home</a>
        </div>
    </body>
    </html>
    ''')

# Logout Page
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
