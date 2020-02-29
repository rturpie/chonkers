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
URL="http://172.20.32.90:5000"
URL = "http://192.168.43.224:5000"
DRAW_FRAME = 0
CHECK = 0
loc = {}


root = tk.Tk()
root.resizable(False, False)

embed = tk.Frame(root, width = WIDTH, height = HEIGHT_GAME) #creates embed frame for pygame window
embed.grid(columnspan = (WIDTH), rowspan = HEIGHT_GAME) # Adds grid
embed.pack(side = TOP) #packs window to the left


#### creating login canvas
logincanvas = tk.Canvas(root, width = WIDTH, height = HEIGHT_MENU,  relief = 'raised')
logincanvas.pack(expand = YES, fill = BOTH)

# Name of login page
log1 = tk.Label(root, text='Login or SignUp')
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
GBimage = Image.open('goodboy.png')
GBimage = GBimage.resize((32, 32), Image.ANTIALIAS)
GBimage.save('goodboy2.png')
GBimage = PhotoImage(file = 'goodboy2.png')

# stats images
SNACCimage = Image.open('snacc.png')
SNACCimage = SNACCimage.resize((32, 32), Image.ANTIALIAS)
SNACCimage.save('snacc2.png')
SNACCimage = PhotoImage(file = 'snacc2.png')

# good boi images
THE_BOY = Image.open('goodest_boys.png')
THE_BOYS = []
for i in range(29):
    area = (i*64, 0, (i+1)*64, 64)
    THE_BOYS.append(THE_BOY.crop(area))


def world_build(loc,w,h,surf):
    sz = 64

    world = loc["data"]
    for i in range(len(world)):
        row = world[i]
        for r in range(len(row)):
            col = (100,100,100)
            if world[i][r] == "1":
                col = (0,0,0)
            pygame.draw.rect(surf, col, pygame.Rect(i*sz,r*sz,sz,sz))

def draw_player(dir,boys,pos, df):
    print("ummmmmmm")
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
    
    mode = image.mode
    size = image.size
    data = image.tobytes()

    py_image = pygame.image.fromstring(data, size, mode)
    screen.blit(py_image, pos)
        
        



root.update()

os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(LEFT, TOP)

# os.environ['SDL_VIDEODRIVER'] = 'windib'

screen = pygame.display.set_mode((WIDTH,HEIGHT_GAME))
screen.fill(pygame.Color(255,255,255))
image = pygame.image.load(r'0.png')
screen.blit(image, (0, 0))

image = THE_BOYS[1]
mode = image.mode
size = image.size
data = image.tobytes()

py_image = pygame.image.fromstring(data, size, mode)
screen.blit(py_image, (200, 200))

pygame.display.init()
pygame.display.update()

# function to login
def login():
    x1 = str(userbox.get())
    x2 = str(passbox.get())
    params = {"username":x1, "password":x2}
    r = requests.post(url = URL + '/login', data = params)

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

        r = requests.get(URL + "/location", cookies=COOKIES)
        print(r.text)
        global loc
        loc = json.loads(r.text)

        world_build(loc,WIDTH, HEIGHT_GAME, screen)
        global CHECK
        CHECK = 1


        print(loc)



# function to sign in
def signup():
    x1 = str(userbox.get())
    x2 = str(passbox.get())
    params = {"username":x1, "password":x2}
    r = requests.post(url = URL + 'register', data = params)

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


root.update()

while True:
    root.update()
    pygame.display.update()
    if CHECK == 1:
        world_build(loc,WIDTH, HEIGHT_GAME, screen)
        draw_player("RIGHT", THE_BOYS, (200,200),DRAW_FRAME)
        DRAW_FRAME = (DRAW_FRAME + 1)%4
        time.sleep(0.15)
    pass