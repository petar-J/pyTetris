import random

tipovi = {
    "I": "0000000011110000",
    "J": "0000100011100000",
    "L": "0000000101110000",
    "O": "0000001100110000",
    "S": "0000001101100000",
    "T": "0000001001110000",
    "Z": "0000011000110000"
}
typeColor = {
    "I": 1,
    "J": 2,
    "L": 3,
    "O": 4,
    "S": 5,
    "T": 6,
    "Z": 7
}

color = [(0, 225, 255), (0, 38, 255), (255, 166, 0), (255, 255, 0), (77, 255, 0), (183, 0, 255), (255, 0, 0)]

slova = ["I","J","L","O","S","T","Z"]

starty = 0

class Block():
    def __init__(self, tip):
        self.type = tip
        self.map = tipovi[self.type]
        self.nextBlockType = slova[random.randint(0, len(slova)-1)]
        self.color = color[typeColor[self.type]-1]
        self.x = 1
        self.y = starty
        self.rot = 0
        self.type = tip


    def collision(self, static):
        for i in range(4):
            for j in range(4):
                #Drawn square
                if(self.getMap(i,j) == 1) :
                    #Out of bounds
                    if(self.x+i < 0 or self.x+i >= len(static) or self.y+j >= len(static[0])):
                        return True
                    #On top of another block
                    if (static[self.x+i][self.y+j] > 0):
                        return True
        return False


    def update(self, static, dy=1):
        #Move to next pos
        self.y += dy
        #Go back if collided
        if(self.collision(static)):
            self.y -= dy
            #Put block in static
            if(dy == 1):
                for i in range(4):
                    for j in range(4):
                        if(self.getMap(i, j) == 1):
                            static[self.x+i][self.y+j] = typeColor[self.type]
                #Make new block
                self.reset(static)
            return 1
        return 0


    def side(self, static, d):
        #Move
        self.x += d
        #Go back if collided
        if(self.collision(static)):
            self.x -= d
            return 1
        return 0


    def rotate(self, static):
        if(self.map == tipovi["O"]): return
        
        self.rot += 1
        self.rot %= 4
        if(self.collision(static)):
            self.rot -= 1
            self.rot %= 4
            return 1
        return 0


    def reset(self, static):
        self.type = self.nextBlockType
        self.map = tipovi[self.type]
        self.nextBlockType = slova[random.randint(0, len(slova)-1)]
        self.color = color[typeColor[self.type]-1]
        self.x = 3
        self.y = starty
        self.rot = 0

        if(self.collision(static)):
            self.y -= 1
            if(self.collision(static)):
                self.y -= 1


    def getMap(self, j, i):
        #j pa i zbog jbg
        if(self.rot == 0):
            # Right side up
            return int(self.map[j*4+i])
        elif(self.rot == 1):
            # u desno rotirano
            return int(self.map[i*4+3-j])
        elif(self.rot == 2):
            # Upside down
            return int(self.map[(3-j)*4+3-i])
        elif(self.rot == 3):
            # u levo
            return int(self.map[(3-i)*4+j])

    def draw(self, area):
        for i in range(4):
            for j in range(4):
                if(self.getMap(i,j) == 1):
                    if(self.x+i >= 0 and self.y+j >= 0):
                        area[self.x+i][self.y+j] = 1


    def goToBottom(self, static):
        while not self.collision(static):
            self.y += 1
        self.y -= 1
