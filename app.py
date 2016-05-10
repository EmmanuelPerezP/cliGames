import curses 
import copy
import time
import curses.panel 

def main(vent):

    app = mainWindow(vent)
    app.mainLoop()
    

class mainWindow:
    
    objects = []
    
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
        while True:
            self.ventana.addstr(0,0,str(self.mainW.getmaxyx()),curses.color_pair(1))
            self.ventana.noutrefresh()
            entrada = self.mainW.getch()
            player1.move(entrada)
            if entrada == 27:
                break
            i = 0
            while i < len(mainWindow.objects):
                if type(mainWindow.objects[i]) is bullet: 
                    mainWindow.objects[i].updateBullet()
                    if mainWindow.objects[i].currentY == 2:
                        del mainWindow.objects[i]
                        i-=1
                i+=1

            curses.panel.update_panels()
            curses.doupdate()
            time.sleep(0.05)

class player:

    def __init__(self, x=5, y=5):
        width = 5
        height = 3
        self.currentX = x
        self.currentY = y
        #self.mainW = mainW
        self.playerW = curses.newwin(height, width, self.currentY, self.currentX)
        self.playerW.addstr(0,0," /^\ <\-/>", curses.color_pair(1))

        #self.playerW.box()
        self.panelJ = curses.panel.new_panel(self.playerW) 
        #curses.panel.update_panels()
        #self.playerW.noutrefresh()

    def move(self, key_code):

        if key_code == curses.KEY_LEFT:
            self.currentX -= 3
            self.panelJ.move(self.currentY, self.currentX)
            #self.playerW.mvwin(self.currentY, self.currentX)
            #self.playerW.noutrefresh()
            #self.mainW.noutrefresh()

        elif key_code == curses.KEY_RIGHT:
            self.currentX += 3
            self.panelJ.move(self.currentY, self.currentX)
            #self.playerW.mvwin(self.currentY, self.currentX)
            #self.playerW.refresh()
            #self.mainW.noutrefresh()


        elif key_code == curses.KEY_DOWN:
            self.currentY += 2
            self.panelJ.move(self.currentY, self.currentX)
            #self.playerW.mvwin(self.currentY, self.currentX)
            #self.playerW.refresh()
            #self.mainW.noutrefresh()
        
        
        elif key_code == curses.KEY_UP:
            self.currentY -= 2
            self.panelJ.move(self.currentY, self.currentX)
            #self.playerW.mvwin(self.currentY, self.currentX)
            #self.playerW.refresh()
            #self.mainW.noutrefresh()
        
        elif key_code == ord(' '):
            bulletFired = bullet(self.currentY, self.currentX)
            mainWindow.objects.append(bulletFired)   

        #curses.panel.update_panels()
        
class bullet:
    
    bulletSpeed = 3
        
    def __init__(self, startingY, startingX, width=2, height=2):
        self.currentX = startingX +2
        self.currentY = startingY -2

        self.width = width 
        self.height = height 
        self.bulletW = curses.newwin(height, width, self.currentY, self.currentX) 
        self.bulletW.addstr('|')
        self.bulletP = curses.panel.new_panel(self.bulletW) 
        self.speed = 0 

    def updateBullet(self):
        if self.speed != bullet.bulletSpeed:
            self.speed+=1

        elif self.speed == bullet.bulletSpeed:
            
            self.currentY -= 1
            self.bulletP.move(self.currentY, self.currentX)
            self.speed = 0
            


if __name__ == "__main__":
    curses.wrapper(main)
