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
    sizeX = 0
    sizeY = 0

    def __init__(self, mainW):
        self.mainW = mainW
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, 5, -1)
        self.mainW.nodelay(True)
    
    def mainLoop(self):
        player1 = player(7, 7)
        self.ventana = curses.newwin(10, 10, 0, 0)
        self.objects.append(self.ventana)
        self.objects.append(player1)
        curses.curs_set(0)
        mainWindow.sizeX = self.mainW.getmaxyx()[1]
        self.mainW.box()
        while True:
            #self.ventana.addstr(0,0,str(self.mainW.getmaxyx()),curses.color_pair(1))
            self.ventana.addstr(0,0,str(mainWindow.sizeX),curses.color_pair(1))
            self.ventana.noutrefresh()
            agregarEnemigos = random.randint(0,70)
            if agregarEnemigos == 5:
                self.addEnemies()
            entrada = self.mainW.getch()
            player1.move(entrada)
            if entrada == 27:
                break
           
            i = 0
            while i < len(mainWindow.bullets):
                mainWindow.bullets[i].updateBullet()
                i+=1

            i = 0
            while i < len(mainWindow.enemies):
                mainWindow.enemies[i].updateEnemy()
                i+=1
                
            curses.panel.update_panels()
            curses.doupdate()
            time.sleep(0.02)

    def addEnemies(self):
        newEnemies = random.randint(1,3) 
        for i in range(0,newEnemies):
            enemyX = random.randint(1, 28)
            enemyY = random.randint(1, 29)
            enemy1(enemyX, enemyY)
        

class player:

    Xsteps = 3
    Ysteps = 2

    def __init__(self, x=5, y=5):
        width = 5
        height = 3
        self.currentX = x
        self.currentY = y
        self.playerW = curses.newwin(height, width, self.currentY, self.currentX)
        self.playerW.addstr(0,0," /^\ <\-/>", curses.color_pair(1))
        self.panelJ = curses.panel.new_panel(self.playerW) 

    def move(self, key_code):
        
        if key_code == curses.KEY_LEFT:
            self.currentX -= player.Xsteps
            self.panelJ.move(self.currentY, self.currentX)

        elif key_code == curses.KEY_RIGHT:
            self.currentX += player.Xsteps
            self.panelJ.move(self.currentY, self.currentX)

        elif key_code == curses.KEY_DOWN:
            self.currentY += player.Ysteps
            self.panelJ.move(self.currentY, self.currentX)
        
        elif key_code == curses.KEY_UP:
            self.currentY -= player.Ysteps 
            self.panelJ.move(self.currentY, self.currentX)
        
        elif key_code == ord(' '):
            bulletFired = bullet(self.currentY, self.currentX, len(mainWindow.bullets))


class enemy1:

    speed = 3

    def __init__(self, startingY, startingX):

        self.currentX = startingX 
        self.currentY = startingY 


        self.width = 3 
        self.height = 3 
        self.enemy1W = curses.newwin(self.height, self.width, self.currentY, self.currentX) 
        self.enemy1W.addstr('<=>~.~')
        self.enemy1P = curses.panel.new_panel(self.enemy1W) 
        self.speed = 0 
        self.direccion = 1
        
        mainWindow.enemies.append(self)

    def updateEnemy(self):

        for i in mainWindow.bullets:
            if self.currentX+2 >= i.currentX >= self.currentX and \
                    self.currentY-2 <= i.currentY <=self.currentY:
                        try:
                            mainWindow.enemies.remove(self)
                        except:
                            pass


        if self.speed != enemy1.speed:
            self.speed +=1


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
    
    bulletSpeed = 1
        
    def __init__(self, startingY, startingX, index, width=1, height=2):
        self.currentX = startingX +2
        self.currentY = startingY -2

        self.width = width 
        self.height = height 
        self.bulletW = curses.newwin(height, width, self.currentY, self.currentX) 
        self.bulletW.addstr('|')
        #self.bulletW.box()
        self.bulletP = curses.panel.new_panel(self.bulletW) 
        self.speed = 0 
        
        self.index = index
        mainWindow.bullets.append(self)

    def updateBullet(self):

        if self.currentY == 1:
            mainWindow.bullets.remove(self)

        if self.speed != bullet.bulletSpeed:
            self.speed+=1

        elif self.speed == bullet.bulletSpeed:
            
            self.currentY -= 1
            self.bulletP.move(self.currentY, self.currentX)
            self.speed = 0
            


if __name__ == "__main__":
    curses.wrapper(main)
