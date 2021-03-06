import curses 
import random
import copy
import time
import curses.panel 

def main(vent):

    app = mainWindow(vent)
    app.mainLoop()
    

class mainWindow:
    
    enemies = []
    bullets = []
    objects = []
    players = []
    sizeX = 0
    sizeY = 0
    score = 0

    def __init__(self, mainW):
        self.mainW = mainW
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, 5, -1)
        curses.init_pair(2, 2, -1)
        curses.init_pair(3, 7, -1)
        self.mainW.nodelay(True)
        mainWindow.sizeX = self.mainW.getmaxyx()[1]
        mainWindow.sizeY = self.mainW.getmaxyx()[0]

    def mainLoop(self):
        player(mainWindow.sizeY//2, mainWindow.sizeX//2)
        self.ventana = curses.newwin(10, 10, 0, 0)
        self.objects.append(self.ventana)
        curses.curs_set(0)
        mainWindow.sizeX = self.mainW.getmaxyx()[1]
        self.mainW.box()
        self.addEnemies()
        while True:

            mainWindow.sizeX = self.mainW.getmaxyx()[1]
            mainWindow.sizeY = self.mainW.getmaxyx()[0]

            #:self.ventana.addstr(0,1,str(mainWindow.score),curses.color_pair(1))
            self.ventana.addstr(0,0,str("|" * player.lifePoints),curses.color_pair(1))
            self.ventana.noutrefresh()
            agregarEnemigos = random.randint(0,500)
            if agregarEnemigos == 50:
                self.addEnemies()
            entrada = self.mainW.getch()
            #self.ventana.addstr(0,0,str(entrada),curses.color_pair(1))
            if entrada == 27:
                break
            if entrada == ord('n'):
                player(mainWindow.sizeY//2, mainWindow.sizeX//2)

            for i in mainWindow.players:
                i.move(entrada) 
            for i in mainWindow.bullets:
                i.update()
                i.render()
            for i in mainWindow.enemies:
                i.updateEnemy()
            for i in mainWindow.players:
                i.updatePlayer()
                
            curses.panel.update_panels()
            curses.doupdate()
            time.sleep(0.006)

    def addEnemies(self):
        newEnemies = random.randint(1,3) 
        for i in range(0,newEnemies):
            enemyX = random.randint(1, mainWindow.sizeX - 5)
            enemyY = random.randint(1, mainWindow.sizeY - 4)
            enemy1(enemyY, enemyX)
        

class player:

    Xsteps = 1
    Ysteps = 1
    speed = 6 
    lifePoints = 10
    releaseKeys = [ -11, -10, -18, -19]

    def __init__(self, y, x):
        width = 5
        height = 3
        self.currentX = x
        self.currentY = y
        self.dirX = 0
        self.dirY = 0
        self.stop = True
        player.lifePoints = 10

        self.playerW = curses.newwin(height, width, self.currentY, self.currentX)
        self.playerW.addstr(0,0," /^\ <\-/>", curses.color_pair(1))
        self.panelJ = curses.panel.new_panel(self.playerW) 
        self.speed = 0
        mainWindow.players.append(self)


    def updatePlayer(self):
        """
        updates the player on screen, it has a delay so its independent of the 
        refresh rate
        """
        for bullet in mainWindow.bullets:
            if self.currentX <= bullet.currentX <= self.currentX+3 and \
                    self.currentY <= bullet.currentY <=self.currentY+6 and \
                    bullet.getEnemy() == "enemy":
                        if player.lifePoints == 0:
                            try:
                                mainWindow.players.remove(self)
                            except:
                                pass
                        else:
                            player.lifePoints -= 1

        if self.speed != player.speed:
            self.speed += 1
        elif self.speed == player.speed:

            if self.dirX == -1:
                self.currentX-=player.Xsteps
            elif self.dirX == 1:
                self.currentX+=player.Xsteps
            elif self.dirX == 0:
                pass
            
            if self.currentX == mainWindow.sizeX-5 or self.currentX == 4:
                self.dirX = 0

            if self.dirY == -1:
                self.currentY-=player.Ysteps
            elif self.dirY == 1:
                self.currentY+=player.Ysteps
            elif self.dirY == 0:
                pass
            
            if self.currentY == mainWindow.sizeY -4 or self.currentY == 2:
                self.dirY = 0

            if self.stop == False:
                self.dirX = 0
                self.dirY = 0
                self.stop = True
    

            self.panelJ.move(self.currentY, self.currentX)
            self.speed = 0


    def move(self, key_code):
        """
        alters the state of the player acording to the key_code (key pressed)
        its independent of updatePlayer 
        if self.currentX == mainWindow.sizeX-5:
            if key_code == curses.KEY_LEFT:
                self.currentX -= player.Xsteps
        elif self.currentX == 5:
            if key_code == curses.KEY_RIGHT:
                self.currentX += player.Xsteps
        elif self.currentY == 5:
            if key_code == curses.KEY_DOWN:
                self.currentY += player.Ysteps 
        elif self.currentY == mainWindow.sizeY-5:
            if key_code == curses.KEY_UP:
                self.currentY -= player.Ysteps  
        """

        if key_code == curses.KEY_LEFT:
            if self.currentX == 4:
                self.dirX = 0
            else:
                self.dirX = -1
        elif key_code == curses.KEY_RIGHT:
            if self.currentX == mainWindow.sizeX-4:
                self.dirX = 0
            else:
                self.dirX = 1
        elif key_code == curses.KEY_DOWN:
            if self.currentY == mainWindow.sizeY -4:
                self.dirY = 0
            else:
                self.dirY = 1
        elif key_code == curses.KEY_UP:
            if self.currentY == 2:
                self.dirY = 0
            else:
                self.dirY = -1

        elif key_code == ord(' '):
            bulletFired = bullet(self.currentY, self.currentX,
                    len(mainWindow.bullets), 2, "player")

        elif key_code == ord('s'):
            self.stop = not self.stop


class enemy1:

    speed = 80
    bulletFrequency = 200

    def __init__(self, startingY, startingX):

        self.currentX = startingX 
        self.currentY = startingY 
        self.bulletFrequency = 0


        self.width = 3 
        self.height = 3 
        self.enemy1W = curses.newwin(self.height, self.width, self.currentY, self.currentX) 
        self.enemy1W.addstr('<=><H>')
        self.enemy1P = curses.panel.new_panel(self.enemy1W) 
        self.speed = 0 
        self.direccion = 1
        
        mainWindow.enemies.append(self)

    def updateEnemy(self):

        for bulletInField in mainWindow.bullets:
            if self.currentX <= bulletInField.currentX <= self.currentX+2 and \
                    self.currentY-2 <= bulletInField.currentY <=self.currentY \
                    and bulletInField.getEnemy() == "player":
                        try:
                            mainWindow.enemies.remove(self)
                            mainWindow.score +=1
                        except:
                            pass


        if self.speed != enemy1.speed:
            self.speed +=1
            self.bulletFrequency +=1


        if self.bulletFrequency == enemy1.bulletFrequency:
            bulletFired = bullet(self.currentY+4, self.currentX,
                    len(mainWindow.bullets), 3, "enemy", 1)
            self.bulletFrequency = 0


        elif self.speed == enemy1.speed:

            if self.direccion == 1:
                self.currentX += 1 
            elif self.direccion == -1:
                self.currentX -= 1 

            if self.currentX == mainWindow.sizeX-4: #es -4 por el tamano 
                self.direccion = -1
            elif self.currentX == 1:
                self.direccion = 1
            self.enemy1P.move(self.currentY, self.currentX)
            self.speed = 0

class bullet:
    
    # smaller value faster speed
    bulletSpeed = 4
        
    def __init__(self, startingY, startingX, index, color, thrower, direction=-1, width=1, height=2):
        self.currentX = startingX +2
        self.currentY = startingY -2
        self.direction = direction
        self.thrower = thrower

        self.width = width 
        self.height = height 
        self.bulletW = curses.newwin(height, width, self.currentY, self.currentX) 
        self.bulletW.addstr('|', curses.color_pair(color))
        #self.bulletW.box()
        self.bulletP = curses.panel.new_panel(self.bulletW) 
        self.speed = 0 
        
        self.index = index
        mainWindow.bullets.append(self)

    def speed(self):
        if self.speed != bullet.bulletSpeed:
            self.speed+=1

    def update(self):
        if self.currentY == 0 or self.currentY == mainWindow.sizeY-2:
            mainWindow.bullets.remove(self)
        elif self.speed == bullet.bulletSpeed:
            if self.direction == -1: 
                self.currentY -= 1
            elif self.direction == 1:
                self.currentY += 1
            self.speed=0
        self.speed+=1

    def render(self):
        self.bulletP.move(self.currentY, self.currentX)

    def getEnemy(self):
        return self.thrower
            


if __name__ == "__main__":
    curses.wrapper(main)
