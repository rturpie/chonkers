from app import app
from app import db
from flask_login import current_user, login_user
from app.models import User, Location
from flask import request
import json

@app.route('/')
def index():
    return "hello world!"

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    user_name  = User.query.filter_by(username=username).first()
    if user_name:
        return "username in use"
    
    # create new user with the form data.
    new_user = User(username=username)
    new_user.set_password(password)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return "successfully registered"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    hub = Location.query.filter_by(name="hub").first()
    user = User.query.filter_by(username=username).first()
    
    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not user.check_password(password): 
        print("User %s has invalid credentials" % username)
        return "invalid credentials"    
    
    user.location = hub.id
    db.session.commit()

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    print("User %s has logged in" % username)
    return "successful login"

@app.route('/location', methods=['GET'])
def location():
    if not current_user.is_authenticated:
        return "user not authenticated"

    loc_id = current_user.location
    loc_name = Location.query.filter_by(id=loc_id).first().name
    loc_file = open('locations/%s.map' % loc_name)
    lines = loc_file.readlines()
    loc_file.close()
    lines = list(map(lambda z: z.strip(), lines))
    out = {'data': lines} 
    return json.dumps(out)
    
    


    
    