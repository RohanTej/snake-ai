import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        



class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self, direction):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        
        if direction == 'LEFT':
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif direction == 'RIGHT':
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif direction == 'UP':
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif direction == 'DOWN':
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)

    def move_computer(self, snack):
        # get distance between snake's head and snack       
        distance = math.sqrt((self.head.pos[0]-snack.pos[0])**2+(self.head.pos[1]-snack.pos[1])**2)

        # make snake turn to where the distance to snack is least
        # make a psudo move to find where it would move next
        dict_of_distance = {}

        # left
        new_distance = math.sqrt((self.head.pos[0]-snack.pos[0]-1)**2+(self.head.pos[1]-snack.pos[1])**2)
        dict_of_distance['LEFT'] =  new_distance

        # right
        new_distance = math.sqrt((self.head.pos[0]-snack.pos[0]+1)**2+(self.head.pos[1]-snack.pos[1])**2)
        dict_of_distance['RIGHT'] =  new_distance

        # up
        new_distance = math.sqrt((self.head.pos[0]-snack.pos[0])**2+(self.head.pos[1]-snack.pos[1]-1)**2)
        dict_of_distance['UP'] =  new_distance

        # down
        new_distance = math.sqrt((self.head.pos[0]-snack.pos[0])**2+(self.head.pos[1]-snack.pos[1]+1)**2)
        dict_of_distance['DOWN'] =  new_distance
        
        # commit that move
        for iterator_distance in sorted(dict_of_distance.values()):
            # check if there is a collision with body
            collision_flag = 0
            key_list = list(dict_of_distance.keys())
            new_direction = key_list[list(dict_of_distance.values()).index(iterator_distance)]
            print(new_direction)


            dx, dy = self.head.dirnx, self.head.dirny
            if dx == 1 and dy == 0 and new_direction == 'LEFT':
                for x in range(len(self.body)):
                    print("test", self.head.pos[0]+1, self.body[x].pos[0])
                    if self.head.pos[0]+1 == self.body[x].pos[0] or self.head.pos[0]-1 == self.body[x].pos[0]:
                        collision_flag = 1
            elif dx == -1 and dy == 0 and new_direction == 'RIGHT':
                for x in range(len(self.body)):
                    print("test", self.head.pos[0]-1, self.body[x].pos[0])
                    if self.head.pos[0]-1 == self.body[x].pos[0] or self.head.pos[0]+1 == self.body[x].pos[0]:
                        collision_flag = 1
            elif dx == 0 and dy == 1 and new_direction == 'UP':
                for x in range(len(self.body)):
                    print("test", self.head.pos[1]+1, self.body[x].pos[1])
                    if self.head.pos[1]+1 == self.body[x].pos[1] or self.head.pos[1]-1 == self.body[x].pos[1]:
                        collision_flag = 1
            elif dx == 0 and dy == -1 and new_direction == 'DOWN':
                for x in range(len(self.body)):
                    print("test", self.head.pos[1]-1, self.body[x].pos[1])
                    if self.head.pos[1]-1 == self.body[x].pos[1] or self.head.pos[1]+1 == self.body[x].pos[1]:
                        collision_flag = 1

            # if collision is detected, check for the next shortest move
            if collision_flag:
                continue
            else:
                self.move(new_direction)
                break

        # debug
        print(self.head.pos[0], self.head.pos[1], " + ", snack.pos[0], snack.pos[1], distance)

        

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        self.addCube()
        self.addCube()


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
        

def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows, surface)
    pygame.display.update()


def randomSnack(rows, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    flag = True

    clock = pygame.time.Clock()
    
    s.addCube()
    s.addCube()
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move_computer(snack)
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0,255,0))

        # check for snake collision with it's own body
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((10,10))
                break

            
        redrawWindow(win)

main()