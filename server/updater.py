from app import app, db
from app.models import User, Location, Entity
from datetime import datetime
import cavegen
import time

ready_countdown = 0
ready = []

def update_aliveness():
    users = User.query.filter_by(is_alive=True)   
    cur = datetime.now() 
    for u in users:
        dt = (cur - u.last_active).total_seconds()
        print(dt)
        if dt > 60*10:
            u.is_alive = False
            db.session.commit()
        if dt > 0.5:
            u.direction = "STILL"

# get all the entities for a location
def get_entities(location):
    return []

def get_location(user):
    loc_id = user.location
    loc = Location.query.filter_by(id=loc_id).first()
    loc_name = loc.name
    loc_file = open('locations/%s.map' % loc_name)
    lines = loc_file.readlines()
    loc_file.close()
    lines = list(map(lambda z: z.strip(), lines))
    location = []
    for row in lines:
        location.append(list(map(int, row)))
    return location

def do_actions():
    users = User.query.filter_by(is_alive=True)
    for u in users:
        action = u.action
        if action != "":
            location = u.location
            entities = Entity.query.filter_by(location=location)
            for e in entities:
                ex,ey = map(int,e.position.split(','))
                ux,uy = map(int,u.position.split(','))
                if (ux-ex)**2 + (uy-ey)**2 <= 2:
                    e.health = e.health - 1
                    if e.health <= 0:
                        u.xp += 50
                        if e.type == "c":
                            pass
                            # go back to start island
                        db.session.delete(e)
                        

                

def check_ready():
    global ready
    if len(ready) > 0 and time.time() - ready_countdown > 4:
        users = []
        print("Ready!!")
        for r in ready:
            print ("%s ready" % r)
            u = User.query.filter_by(username=r).first()
            users.append(u)

        avg = sum(map(lambda x: x.level, users)) // len(users) + 1
        cave_name, init, chest, enemies = cavegen.generate_cave([0,1], avg)
        cave = Location(name=cave_name, init_pos="%s,%s" % (init[0],init[1]))
        chest = Entity(name="chest",type="c",health=1,location=cave.id, position="%s,%s"%(chest[0],chest[1]))
        db.session.add(cave)
        db.session.commit()
        for ex,ey,name in enemies:
            print(ex,ey,name)
            print()
            e = Entity(name=name,type="e",health=avg,location=cave.id, position="%s,%s" % (ex,ey))
            db.session.add(e)
        for u in users:
            u.location = cave.id
            u.position = cave.init_pos
        ready = []
        db.session.commit()


def update_positions():
    invalid_blocks = [0,3]
    users = User.query.filter_by(is_alive=True)
    print("updating positions")
    for u in users:
        location = get_location(u)
        x,y = map(int, (u.position).split(','))

        # TODO CHECK FOR PLAYER IN THE WAY
        if u.direction == "LEFT":
            x -= 1
            if location[y][x] in invalid_blocks:
                print(location[y][x])
                x+=1
        if u.direction == "RIGHT":
            x += 1
            if location[y][x] in invalid_blocks:
                x-=1
        if u.direction == "UP":
            y -= 1
            if location[y][x] in invalid_blocks:
                y+=1
        if u.direction == "DOWN":
            y += 1
            if location[y][x] in invalid_blocks:
                y-=1
        u.position = "%d,%d" % (x,y)

        global ready
        global ready_countdown
        # check if player is in dungeon ready area
        if u.location == 1:
            if x > 8 and x <= 12 and y < 10:
                if not (u.username in ready):
                    ready.append(u.username)
                    ready_countdown = time.time()
    db.session.commit()

# game loop
while True:
    update_aliveness()
    update_positions()
    check_ready()
    do_actions()
    time.sleep(0.5)
    
        
