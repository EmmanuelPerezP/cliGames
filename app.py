import curses 
import curses.panel 

def main(vent):

    app = mainWindow(vent)
    app.mainLoop()
    

class mainWindow:
    
    def __init__(self, mainW):
        self.mainW = mainW
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, 10, -1)
        self.mainW.nodelay(True)
        
    
    def mainLoop(self):
        player1 = player(self.mainW, 7, 7)
        self.ventana = curses.newwin(10, 10, 0, 0)
        while True:
            self.ventana.addstr(0,0,str(self.mainW.getmaxyx()),curses.color_pair(1))
            self.ventana.noutrefresh()
            entrada = self.mainW.getch()
            player1.move(entrada)
            if entrada == 27:
                break
            curses.doupdate()
            

class player:

    def __init__(self, mainW, x=5, y=5):
        width = 5
        height = 3
        self.currentX = x
        self.currentY = y
        self.mainW = mainW
        self.playerW = curses.newwin(height, width, self.currentY, self.currentX)
        self.playerW.addstr(0,0,"<^^^><--->")
        #self.playerW.box()
        self.panelJ = curses.panel.new_panel(self.playerW) 
        curses.panel.update_panels()
        self.playerW.noutrefresh()

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
            

        curses.panel.update_panels()
        


if __name__ == "__main__":
    curses.wrapper(main)

