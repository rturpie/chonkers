import pygame
import tkinter as tk
from tkinter import *
import os
import requests
import json
from PIL import Image

WIDTH = 1000
HEIGHT_GAME = 700
HEIGHT_MENU = 300
COOKIES = []
URL="http://172.20.32.90:5000"

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

# function to login
def login():
    x1 = str(userbox.get())
    x2 = str(passbox.get())
    params = {"username":x1, "password":x2}
    r = requests.post(url = 'http://172.20.32.90:5000/login', data = params)

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
        logincanvas.create_image(200, 25, image=HEALTHimage, anchor=NW)
        logincanvas.create_image(233, 25, image=GBimage, anchor=NW)

        r = requests.get(URL + "/location", cookies=COOKIES)
        print(r.text)
        loc = json.loads(r.text)
        print(loc)



# function to sign in
def signup():
    x1 = str(userbox.get())
    x2 = str(passbox.get())
    params = {"username":x1, "password":x2}
    r = requests.post(url = 'http://172.20.32.90:5000/register', data = params)

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

root.update()

os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(LEFT, TOP)

# os.environ['SDL_VIDEODRIVER'] = 'windib'

screen = pygame.display.set_mode((WIDTH,HEIGHT_GAME))
screen.fill(pygame.Color(255,255,255))
image = pygame.image.load(r'0.png')
screen.blit(image, (0, 0))

pygame.display.init()
pygame.display.update()


def draw():
    pygame.draw.circle(screen, (0,0,0), (250,250), 125)
    pygame.display.update()


# button1 = Button(buttonwin,text = 'Draw',  command=draw)
# button1.pack(side=LEFT)


root.update()

while True:
    root.update()
    pass