import sys
sys.path.insert(0,'/home/cwp')
import NEA

if __name__=='__main__':
    app = NEA.gui.guiMain.App(sys.argv)

    app.exec_()
    sys.exit()
