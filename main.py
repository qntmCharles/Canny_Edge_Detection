import sys
sys.path.insert(0,'/home/cwp')
import gui
import canny

if __name__=='__main__':
    app = gui.guiApp.App(sys.argv)

    app.exec_()
    sys.exit()
