from app import app
from app import db
from flask_login import current_user, login_user, logout_user
from app.models import User, Location, Entity
from flask import request
import json
from datetime import datetime

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
    new_user.max_health = 10
    new_user.max_hunger = 10
    new_user.level = 0
    new_user.xp = 0

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
    user.position = hub.init_pos
    user.direction = "STILL"
    user.last_active = datetime.now()
    user.is_alive = True
    user.ready = False
    user.hunger = 10
    if user.max_health == None:
        user.max_health = 10
    if user.max_hunger == None:
        user.max_hunger = 10
    if user.xp == None:
        user.xp = 0
    if user.level == None:
        user.level = 0
    user.health = user.max_health
    db.session.commit()

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    print("User %s has logged in" % username)
    return "successful login"

@app.route('/logout')
def logout():
    logout_user()
    return "logged out"
    

@app.route('/location', methods=['GET'])
def location():
    if not current_user.is_authenticated:
        return "user not authenticated"

    loc_id = current_user.location
    loc = Location.query.filter_by(id=loc_id).first()
    loc_name = loc.name
    loc_file = open('locations/%s.map' % loc_name)
    lines = loc_file.readlines()
    loc_file.close()
    lines = list(map(lambda z: z.strip(), lines))
    out = {'name': loc_name,'data': lines} 
    return json.dumps(out)

@app.route('/stats')
def stats():
    if not current_user.is_authenticated:
        return "user not authenticated"
    health = current_user.health
    max_hp = current_user.max_health
    hunger = current_user.hunger
    max_hunger = current_user.max_hunger
    xp = current_user.xp
    level = current_user.level
    data = {'hp': health, 'max_hp': max_hp, 'xp': xp, 'hunger': hunger, 'max_hunger': max_hunger, 'level': level}
    return json.dumps(data)

@app.route('/entities')
def entities():
    if not current_user.is_authenticated:
        return "user not authenticated"
    users = User.query.filter_by(location=current_user.location, is_alive=True)
    out = {}
    for u in users:
        out[u.username] =   {
                        'type'      : 'p',
                        'location'  : u.location,
                        'direction' : u.direction,
                        'position'  : u.position,
                        }
    entities = Entity.query.filter_by(location=current_user.location)
    for e in entities:
        out[e.name]=    {
                        'type'      : e.type,
                        'location'  : e.location,
                        'position'  : e.position
                        }
    print(out)
    return json.dumps(out)

@app.route('/do_action', methods=['POST'])
def do_action():
    if not current_user.is_authenticated:
        return "user not authenticated"

    current_user.last_active = datetime.now()
    current_user.is_alive = True
    try:
        direction = request.form.get('direction')
    except:
        direction = "STILL"
    try:
        action = request.form.get('action')
    except:
        action = ""
    current_user.direction = direction
    current_user.action    = action
    db.session.commit()
    return "action taken"


    
    