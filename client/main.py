import pygame
import tkinter as tk
from tkinter import *
import os
import requests
import json
from PIL import Image
import time

WIDTH = 1000
HEIGHT_GAME = 700
HEIGHT_MENU = 300
COOKIES = []
URL="http://172.20.40.7:5000"
#URL = "http://192.168.43.224:5000"
#URL="http://localhost:5000"
DRAW_FRAME = 0
CHECK = 0
USERNAME = ""
loc = {}
LOC_ID = 0

back_colours = [[255,237,81],[249,181,209],[117,137,191],[252,169,133]]

pygame.font.init() 
myfont = pygame.font.SysFont('helvetica', 18, bold=True)

root = tk.Tk()
root.resizable(False, False)

embed = tk.Frame(root, width = WIDTH, height = HEIGHT_GAME) #creates embed frame for pygame window
embed.grid(columnspan = (WIDTH), rowspan = HEIGHT_GAME) # Adds grid
embed.pack(side = TOP) #packs window to the left

entities = []


#### creating login canvas
logincanvas = tk.Canvas(root, width = WIDTH, height = HEIGHT_MENU,  relief = 'raised')
logincanvas.pack(expand = YES, fill = BOTH)

# Name of login page
log1 = tk.Label(root, text='Login or Register')
log1.config(font=('helvetica', 14))
logincanvas.create_window(200, 25, window=log1)



# asks for username
user1 = tk.Label(root, text='Username:')
user1.config(font=('helvetica', 10))
logincanvas.create_window(200, 100, window=user1)

# username box
userbox = tk.Entry (root) 
logincanvas.create_window(200, 140, window=userbox)

# asks for password
pass1 = tk.Label(root, text='Password:')
pass1.config(font=('helvetica', 10))
logincanvas.create_window(200, 180, window=pass1)

# password box
passbox = tk.Entry (root) 
logincanvas.create_window(200, 220, window=passbox)


# stats images
HEALTHimage = Image.open('health.png')
HEALTHimage = HEALTHimage.resize((32, 32), Image.ANTIALIAS)
HEALTHimage.save('health2.png')
HEALTHimage = PhotoImage(file = 'health2.png')

# stats images
# HEALTHimage = Image.open('health.png')
# HEALTHimage = HEALTHimage.resize((32, 32), Image.ANTIALIAS)
# HEALTHimage.save('health2.png')
CHONKERSimage = PhotoImage(file = 'chonkers.png')

# stats images
CHESTimage = Image.open('chest.png')
CHESTimage = CHESTimage.resize((64, 64), Image.ANTIALIAS)
CHESTimage.save('chest2.png')
CHESTimage = PhotoImage(file = 'chest2.png')

# stats images
GBimage = Image.open('goodboy.png')
GBimage = GBimage.resize((32, 32), Image.ANTIALIAS)
GBimage.save('goodboy2.png')
GBimage = PhotoImage(file = 'goodboy2.png')

# stats images
SNACCimage = Image.open('snacc.png')
SNACCimage = SNACCimage.resize((32, 32), Image.ANTIALIAS)
SNACCimage.save('snacc2.png')
SNACCimage = PhotoImage(file = 'snacc2.png')

# skeleton facing left image
SKELLYLimage = Image.open('skellyl.png')
SKELLYLimage = SKELLYLimage.resize((64, 64), Image.ANTIALIAS)
SKELLYLimage.save('skellyl2.png')
SKELLYLimage = pygame.image.load('skellyl2.png')


# skeleton facing right image
SKELLYRimage = Image.open('skellyr.png')
SKELLYRimage = SKELLYRimage.resize((64, 64), Image.ANTIALIAS)
SKELLYRimage.save('skellyr2.png')
SKELLYRimage = pygame.image.load('skellyr2.png')

# cat facing left image
CATLimage = Image.open('catl.png')
CATLimage = CATLimage.resize((64, 64), Image.ANTIALIAS)
CATLimage.save('catl2.png')
CATLimage = pygame.image.load('catl2.png')


# cat facing right image
CATRimage = Image.open('catr.png')
CATRimage = CATRimage.resize((64, 64), Image.ANTIALIAS)
CATRimage.save('catr2.png')
CATRimage = pygame.image.load('catr2.png')

# water texture
WATERimage = Image.open('water_still.png')
WATERimage = WATERimage.resize((64, 64), Image.ANTIALIAS)
WATERimage.save('water_still.png')
WATERimage = pygame.image.load('water_still.png')

# sand texture
SANDimage = Image.open('sand.png')
SANDimage = SANDimage.resize((64, 64), Image.NEAREST)
SANDimage.save('sand.png')
SANDimage = pygame.image.load('sand.png')

DOORimage = Image.open('door.png')
DOORimage = DOORimage.resize((64,64), Image.NEAREST)
DOORimage.save('door2.png')
DOORimage = pygame.image.load('door2.png')

STONEimage = Image.open('stone.png')
STONEimage = STONEimage.resize((64,64), Image.NEAREST)
STONEimage.save('stone2.png')
STONEimage = pygame.image.load('stone2.png')


# good boi images
THE_BOY = Image.open('goodest_boys.png')
THE_BOYS = []
for i in range(29):
    area = (i*64, 0, (i+1)*64, 64)
    THE_BOYS.append(THE_BOY.crop(area))


def world_build(loc,w,h,surf,offset):
    sz = 64
    x, y = offset

    world = loc["data"]
    for i in range(len(world)):
        row = world[i]
        for r in range(len(row)):
            tex = WATERimage
            if world[i][r] == "1":
                tex = SANDimage
            elif world[i][r] == "2":
                tex = STONEimage
            elif world[i][r] == "3":
                tex = DOORimage
            # pygame.draw.rect(surf, col, pygame.Rect(i*sz,r*sz,sz,sz))
            screen.blit(tex, (r*sz - x*sz + WIDTH//2,i*sz - y*sz + HEIGHT_GAME//2))

def draw_player(dir,boys,pos, df):
    x, y = pos
    # print("ummmmmmm")
    if dir == "RIGHT":
        print("rite")
        offset = 4
        image = boys[offset + df]
    if dir == "LEFT":
        offset = 12
        image = boys[offset + df]
    if dir == "UP":
        offset = 8
        image = boys[offset + df]
    if dir == "DOWN":
        offset = 0
        image = boys[offset + df]
    if dir == "STILL":
        offset = 18
        image = boys[offset + (df%2)]
    
    mode = image.mode
    size = image.size
    data = image.tobytes()

    py_image = pygame.image.fromstring(data, size, mode)
    screen.blit(py_image, (x*64 + WIDTH//2,y*64 + HEIGHT_GAME//2))

def draw_skeleton(pos, df):
    px, py = pos
    if df%2 == 0:
        screen.blit(SKELLYLimage, (px*64 + WIDTH//2,py*64 + HEIGHT_GAME//2))
    if df%2 ==1:
        screen.blit(SKELLYRimage, (px*64 + WIDTH//2,py*64 + HEIGHT_GAME//2))

def draw_cat(pos, df):
    if df%2 == 0:
        screen.blit(CATRimage, pos)
    if df%2 ==1:
        screen.blit(CATLimage, pos)

def draw_chest(pos, df):
    screen.blit(CHESTimage, pos)

        
        



root.update()

os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(LEFT, TOP)

# os.environ['SDL_VIDEODRIVER'] = 'windib'

screen = pygame.display.set_mode((WIDTH,HEIGHT_GAME))
screen.fill(pygame.Color(back_colours[DRAW_FRAME][0],back_colours[DRAW_FRAME][1],back_colours[DRAW_FRAME][2]))
image = pygame.image.load(r'0.png')
#screen.blit(image, (0, 0))

# log
CHONKimage = Image.open('chonkers.png')
CHONKimage = CHONKimage.resize((800, 200), Image.NEAREST)
CHONKimage.save('chonkers2.png')
CHONKimage = pygame.image.load('chonkers2.png')

logo = pygame.image.load(r'chonkers2.png')
screen.blit(logo, (100,100))

image = THE_BOYS[1]
mode = image.mode
size = image.size
data = image.tobytes()

py_image = pygame.image.fromstring(data, size, mode)
# screen.blit(py_image, (200, 200))

pygame.display.init()
pygame.display.update()

def get_stats():
    r = requests.get(URL + '/stats', cookies = COOKIES)
    return json.loads(r.text)

def get_location():
    r = requests.get(URL + "/location", cookies=COOKIES)
    return json.loads(r.text)

def logout():
    pass

# function to login
def login():
    x1 = str(userbox.get())
    x2 = str(passbox.get())
    global USERNAME
    USERNAME = x1
    params = {"username":x1, "password":x2}
    r = requests.post(url = URL + '/login', data = params)

    global COOKIES
    COOKIES = r.cookies

    clear = tk.Label(root, text='                                                                                                                            ')
    clear.config(font=('helvetica', 10))
    logincanvas.create_window(200, 300, window=clear)
    if r.text == "invalid credentials":
        error = tk.Label(root, text='Sorry, your username or password is incorrect.')
        error.config(font=('helvetica', 10))
        logincanvas.create_window(200, 300, window=error)
    else:
        success = tk.Label(root, text='YEET - *DOES SOMETHING*.')
        success.config(font=('helvetica', 10))
        logincanvas.create_window(200, 300, window=success)
        logincanvas.delete("all")
        logincanvas.create_image(20, 200, image=HEALTHimage, anchor=NW)
        logincanvas.create_image(20, 233, image=GBimage, anchor=NW)
        logincanvas.create_image(20, 266, image=SNACCimage, anchor=NW)

        logoutbutton = tk.Button(text='Log OUt', command=logout)
        logincanvas.create_window(930, 270, window=logoutbutton)



        r = requests.get(URL + "/location", cookies=COOKIES)
        global loc
        loc = json.loads(r.text)


        stats = get_stats()
        hp = stats['hp']
        max_hp = stats['max_hp']
        xp = stats['xp']
        hunger = stats['hunger']
        max_hunger = stats['max_hunger']

        # health
        u = "HEALTH: " + str(hp) + "/" + str(max_hp)
        user1 = tk.Label(root, text= u)
        user1.config(font=('helvetica', 10))
        logincanvas.create_window(130, 210, window=user1)

        # good boy
        u = "GOOD BOY POINTS: " + str(xp)
        user1 = tk.Label(root, text= u)
        user1.config(font=('helvetica', 10))
        logincanvas.create_window(150, 240, window=user1)

        # health
        u = "SNACC LEVEL: " + str(hunger) + "/" + str(max_hunger)
        user1 = tk.Label(root, text= u)
        user1.config(font=('helvetica', 10))
        logincanvas.create_window(150, 275, window=user1)

        world_build(loc,WIDTH, HEIGHT_GAME, screen, (0,0))
        global CHECK
        CHECK = 1


        print(loc)



# function to sign in
def signup():
    x1 = str(userbox.get())
    x2 = str(passbox.get())
    params = {"username":x1, "password":x2}
    r = requests.post(url = URL + '/register', data = params)

    clear = tk.Label(root, text='                                                                                                                          ')
    clear.config(font=('helvetica', 10))
    logincanvas.create_window(200, 300, window=clear)
    if r.text == "username in use":
        error = tk.Label(root, text='Sorry, that username has already been taken.')
        error.config(font=('helvetica', 10))
        logincanvas.create_window(200, 300, window=error)
    else:
        success = tk.Label(root, text='Congratulations, you have successfully registered. Now Log In.')
        success.config(font=('helvetica', 10))
        logincanvas.create_window(200, 300, window=success)        

    print(r.text)
    print(x1)
    print(x2)


loginbutton = tk.Button(text='login', command=login)
logincanvas.create_window(160, 260, window=loginbutton)

signupbutton = tk.Button(text='register', command=signup)
logincanvas.create_window(240, 260, window=signupbutton)

buttonwin = tk.Frame(root, width = 75, height = 500)
buttonwin.pack(side = LEFT)




def draw():
    pygame.draw.circle(screen, (0,0,0), (250,250), 125)
    pygame.display.update()


# button1 = Button(buttonwin,text = 'Draw',  command=draw)
# button1.pack(side=LEFT)
def get_entities(cookies):
    r = requests.get(URL + '/entities', cookies=cookies)
    entities = json.loads(r.text)
    return entities


root.update()
last = time.time()
last2 = time.time()

def send_action(key):
    print (key.keysym)
    if key.keysym == "w":
        data={'direction':'UP'}
        r = requests.post(URL+"/do_action", cookies=COOKIES, data=data)
        print (r.text)
    if key.keysym == "a":
        data={'direction':'LEFT'}
        r = requests.post(URL+"/do_action", cookies=COOKIES, data=data)
        print (r.text)
    if key.keysym == "s":
        data={'direction':'DOWN'}
        r = requests.post(URL+"/do_action", cookies=COOKIES, data=data)
        print (r.text)
    if key.keysym == "d":
        data={'direction':'RIGHT'}
        r = requests.post(URL+"/do_action", cookies=COOKIES, data=data)
        print (r.text)

os.system('xset r off')
root.bind("<KeyPress>",send_action)
# root.bind("<s>",send_action)
# root.bind("<d>",send_action)

temp = 0
counter = 0
while True:
    root.update()
    pygame.display.update()

    if CHECK == 0 and time.time() - last2 > 0.5:
        temp = (temp + 1)%4
        last2 = time.time()
        
    if CHECK == 0 and time.time() - last > 0.15:

        screen.fill(pygame.Color(back_colours[temp][0],back_colours[temp][1],back_colours[temp][2]))
        screen.blit(logo, (100,100))
        logo = pygame.image.load(r'chonkers2.png')
        draw_player("STILL", THE_BOYS, (0,0), DRAW_FRAME)
        DRAW_FRAME = (DRAW_FRAME + 1)%4

    if CHECK == 1 and time.time() - last > 0.15:
        last = time.time()
        entities = get_entities(COOKIES)

        data = entities[USERNAME]
        if data['location'] != LOC_ID:
            loc = get_location()
            LOC_ID = data['location']
        dx,dy = map(int, data['position'].split(','))
        print(dx,dy)
        direction = data['direction']
        world_build(loc,WIDTH, HEIGHT_GAME, screen, (dx,dy))
        for e in entities:
            data = entities[e]
            if e == USERNAME:
                pass
            elif data["type"] == "p":
                px,py = map(int, data['position'].split(','))
                px = px - dx
                py = py - dy
                draw_player(data["direction"], THE_BOYS, (px,py), DRAW_FRAME)
            elif data["type"] == "e":
                px,py = map(int, data['position'].split(','))
                px = px - dx
                py = py - dy
                draw_skeleton((px,py), DRAW_FRAME)
            elif data["type"] == "c":
                px,py = map(int, data['position'].split(','))
                px = px - dx
                py = py - dy
                draw_chest((px,py), DRAW_FRAME)
        draw_player(direction, THE_BOYS, (0,0), DRAW_FRAME)

        for e in entities:
            data = entities[e]
            if (data["type"] == "p" or data["type"] == "e")  and e != USERNAME:
                px,py = map(int, data['position'].split(','))
                px = px - dx
                py = py - dy
                textbox = myfont.render(e, False, (0,0,0))
                screen.blit(textbox, (px*64 + WIDTH//2,py*64 + HEIGHT_GAME//2 - 20))
        textbox = myfont.render(USERNAME, False, (0,0,0))
        screen.blit(textbox, (WIDTH//2,HEIGHT_GAME//2 - 20))
        locbox = myfont.render(loc['name'], False, (180,20,20))
        screen.blit(locbox, (0,0))

        if counter >= 8:
            stats = get_stats()
            hp = stats['hp']
            max_hp = stats['max_hp']
            xp = stats['xp']
            hunger = stats['hunger']
            max_hunger = stats['max_hunger']

            # health
            u = "HEALTH: " + str(hp) + "/" + str(max_hp)
            user1 = tk.Label(root, text= u)
            user1.config(font=('helvetica', 10))
            logincanvas.create_window(130, 210, window=user1)

            # good boy
            u = "GOOD BOY POINTS: " + str(xp)
            user1 = tk.Label(root, text= u)
            user1.config(font=('helvetica', 10))
            logincanvas.create_window(150, 240, window=user1)
            counter = 0

        counter += 1


        # draw_skeleton((200,300), DRAW_FRAME)
        # draw_cat((250,350),DRAW_FRAME)
        DRAW_FRAME = (DRAW_FRAME + 1)%4
