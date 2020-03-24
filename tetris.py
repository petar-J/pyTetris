import pygame as pg
import sys, random
from Block import Block, tipovi, color, typeColor
from copy import deepcopy



def down():
    global area, static, empty, b, pressedKeys
    if(b.update(static) == 1): 
        pressedKeys["Down"] = [0, 0]
    area = deepcopy(empty)
    b.draw(area)

def side(dx):
    global area, static, empty, b, pressedKeys
    k = "Left"
    if(dx == 1): k = "Right"
    if(b.side(static, dx) == 1): 
        pressedKeys[k] = [0, 0]
    area = deepcopy(empty)
    b.draw(area)

def rotate():
    global area, static, empty, b
    if(b.rotate(static) == 1):
        if(b.side(static, -1) == 1):
            if(b.side(static, 1) == 0):
                b.rotate(static)
        else: b.rotate(static)
    area = deepcopy(empty)
    b.draw(area)

def execute(c):
    global paused
    if(c == "Resume"):
        paused = False
    elif(c == "New Game"):
        pass


pg.init()
pg.font.init()
font = pg.font.SysFont("Comic Sans MS", 20)

pressedKeys = {"Down": [0,0],"Left": [0,0],"Right": [0,0]}
keyCodes = {"Down": pg.K_DOWN,"Left": pg.K_LEFT,"Right": pg.K_RIGHT}


width, height = 300, 600
areaW = 10
areaH = 20
blockW = int(width/areaW)
xOffset = blockW*6
yOffset = blockW
screen = pg.display.set_mode((width+2*xOffset, height+yOffset))

area = []

b = Block("T")
ghost = Block(b.type)
nextBlock = Block(b.nextBlockType)


# #Prints moving block
# for i in range(4):
#     for j in range(4):
#         print(b.getMap(i,j), end="")
#     print()

#Makes the area 2d array
for i in range(areaW):
    tmp = []
    for i in range(areaH):
        tmp.append(0)
    area.append(tmp)

#Za blockove koji su sleteli
static = deepcopy(area)
empty = deepcopy(area)

b.draw(area)
#print(area)

gameSpeed = 1000
changeSpeed = 5000
score = 0
lines = 0
gameOver = False
paused = False
pressedDown = 0
pressedDownFor = 0
tetri = []
selected = 0
selections = ["Resume", "New Game"]

frames = 0
while 1:
    #Events -------------------------------------------------------
    for event in pg.event.get():
        if event.type == pg.QUIT: 
            #Save score
            f = open("score.txt", 'a+')
            f.write(str(score)+', '+str(lines)+'\n')
            f.close()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE and not gameOver:
                paused = not paused
            if(not paused and not gameOver):
                if event.key == pg.K_DOWN:
                    down()
                    pressedKeys["Down"][0] = frames
                if event.key == pg.K_LEFT:
                    side(-1)
                    pressedKeys["Left"][0] = frames
                if event.key == pg.K_RIGHT:
                    side(1)
                    pressedKeys["Right"][0] = frames
                if event.key == pg.K_UP:
                    rotate()
            else:
                #Paused
                if event.key == pg.K_UP:
                    selected -= 1
                if event.key == pg.K_DOWN:
                    selected += 1
                if event.key == pg.K_RETURN:
                    execute(selections[selected])
                
    
    if(not paused):
        keys = pg.key.get_pressed()  #checking pressed keys
        if(not gameOver):
            for i in pressedKeys.keys():
                if keys[keyCodes[i]]:
                    if(frames - pressedKeys[i][0] > 200 and pressedKeys[i][0] != 0):
                        pressedKeys[i][1] += 1
                        if(pressedKeys[i][1] % 20 == 0):
                            if(i == "Down"): down()
                            elif(i == "Right"): side(1)
                            elif(i == "Left"): side(-1)
                else:
                    pressedKeys[i] = [0, 0]

                    
        
        #Main loop ---------------------------------------------------------
        if(not gameOver):
            frames += 1
            if(frames % gameSpeed == 0):
                down()
                if(frames % changeSpeed == 0):
                    gameSpeed -= 50
                    print(gameSpeed)
                    if(gameSpeed < 200): gameSpeed = 200
                

            #list of rows which are tetrises
            tetri=[0 for i in range(areaH)]
            for j in range(areaH):
                s = 0
                for i in range(areaW):
                    if(static[i][j] > 0): s+=1
                if(s == areaW):
                    tetri[j] = 1

            # Prints field and tetrises
            # if(1 in tetri):
            #     for j in range(areaH):
            #         for i in range(areaW):
            #             print(static[i][j], end='')
            #         print()
            #     print(tetri)
            for i in reversed(range(len(tetri))):
                if(tetri[i] == 1):
                    score += 200
                    lines += 1
                    for j in range(areaW):
                        del static[j][i:i+1]
            s = sum(tetri)
            for j in range(s):
                for i in range(areaW):
                    static[i] = [0]+static[i]
            

            #Check Game over
            for i in range(areaW):
                if(static[i][1] > 0):
                    gameOver = True
                    print('GameOver')




    #Crtanje ------------------------------------------------------
    screen.fill((255, 255, 255))
        

    ghost.map = b.map
    ghost.color = (200, 200, 200)
    ghost.x = b.x
    ghost.y = b.y
    ghost.rot = b.rot
    ghost.type = b.type
    ghost.goToBottom(static)
    for i in range(4):
        for j in range(4):
            if(ghost.getMap(i, j) == 1):
                pg.draw.rect(screen, ghost.color, (xOffset+(ghost.x+i)*blockW, (ghost.y+j)*blockW, blockW, blockW))

    for i in range(len(area)):
        for j in range(len(area[0])):
            if(area[i][j] > 0):
                pg.draw.rect(screen, b.color, (xOffset+i*blockW, j*blockW, blockW, blockW))
                #screen.fill((0,0,0), (i*blockW, j*blockW, blockW, blockW))
            if(static[i][j] > 0):
                c = color[static[i][j]-1]
                if(tetri[j] == 1): c = (255, 255, 255)
                pg.draw.rect(screen, c, (xOffset+i*blockW, j*blockW, blockW, blockW))
                #screen.fill((0,0,0), (i*blockW, j*blockW, blockW, blockW))
            
    #Next block
    nextBlock.type = b.nextBlockType
    nextBlock.map = tipovi[nextBlock.type]
    nextBlock.color = color[typeColor[nextBlock.type]-1]
    for i in range(4):
        for j in range(4):
            if(nextBlock.getMap(i, j) == 1):
                pg.draw.rect(screen, nextBlock.color, (xOffset+width+(nextBlock.x+i)*blockW, 4*blockW+(nextBlock.y+j)*blockW, blockW, blockW))
    pg.draw.rect(screen, (171, 171, 171), (xOffset+width+blockW, 4*blockW, 4*blockW, 4*blockW), 1)

    #Show score
    scoreText = font.render('Score: '+str(score), True, (0, 0, 0))
    screen.blit(scoreText, (blockW, 4*blockW))
    scoreText = font.render('Lines: '+str(lines), True, (0, 0, 0))
    screen.blit(scoreText, (blockW, 6*blockW))
    
    #Grid lines
    for i in range(len(area)+1):
        pg.draw.line(screen, (171, 171, 171), (xOffset+i*blockW, 0), (xOffset+i*blockW, height))
    for i in range(len(area[0])+1):
        pg.draw.line(screen, (171, 171, 171), (xOffset, i*blockW), (xOffset+width, i*blockW))

    #Pause menu
    if(paused):
        selected %= len(selections)
        startY = 5*blockW
        pg.draw.rect(screen, (94, 94, 94), (xOffset-2*blockW, startY, blockW*(areaW+4), areaH*blockW-2*startY))
        text = font.render("Paused", True, (255, 255, 255))
        screen.blit(text, (xOffset+width//2-text.get_width()//2, blockW+startY-text.get_height()//2))
        for i in range(len(selections)):
            text = font.render(selections[i], True, (200, 200, 200))
            if(i == selected):
                text = font.render(selections[i], True, (0, 0, 0))
                pg.draw.polygon(screen, 0, ((xOffset+width//2-text.get_width()//2-10, (i+4)*blockW+startY),
                                            (xOffset+width//2-text.get_width()//2-15, (i+4)*blockW+startY+5),
                                            (xOffset+width//2-text.get_width()//2-15, (i+4)*blockW+startY-5)))
                pg.draw.polygon(screen, 0, ((xOffset+width//2+text.get_width()//2+10, (i+4)*blockW+startY),
                                            (xOffset+width//2+text.get_width()//2+15, (i+4)*blockW+startY+5),
                                            (xOffset+width//2+text.get_width()//2+15, (i+4)*blockW+startY-5)))
            screen.blit(text, (xOffset+width//2-text.get_width()//2, (i+4)*blockW+startY-text.get_height()//2))

            



    if(gameOver):
        pg.draw.rect(screen, (94, 94, 94), (xOffset-2*blockW, 6*blockW, blockW*(areaW+4), 8*blockW))
        text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(text, (xOffset+width/2-text.get_width()/2, height/2-text.get_height()/2))


    pg.display.flip()
