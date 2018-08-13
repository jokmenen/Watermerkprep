import sys,wmprepgui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel,QSizePolicy
from PyQt5.QtGui import QIcon 


class WMGui(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def callWatermarker(self,selectedFP,selectedWatermark):
        if selectedFP == None:
            print("ERROR: No file or folder slected")
            sys.exit(1)
        else:
            print("Success, calling %s with watermark %s" % (selectedFP,selectedWatermark))


    def selectWatermark(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Image Files (*.png *.jpg *.jpeg)", options=options)
        if filename:
            print(filename, "is set")
            self.selectedWatermark = filename
        else:
            print("Filename Error! Watermark unchanged.")
        self.updateLabels()

    def selectFolder(self): #TODO: Select multiple folders
        options = QFileDialog.Options() #not sure what tbis does lol
        filename  = QFileDialog.getExistingDirectory(self,"Select Folder(s)") #get the file/folder name
        print(filename)
        if filename: #check if file is found, else return error
            print(filename, "is selected as FP")
            self.selectedFP = [filename]
            print(self.selectedFP)
        else:
            print("Filename Error! FP unchanged.")
        self.updateLabels()

    def selectFile(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Image Files (*.png *.jpg *.jpeg)", options=options)
        if filename:
            print(filename, "is selected as FP")
            self.selectedFP = [] + filename
            print(self.selectedFP)
        else:
            print("Filename Error! FP unchanged.")
        self.updateLabels()

    def updateLabels(self):
        self.FPLabel.setText(";\n".join(self.selectedFP))
        self.WMLabel.setText(self.selectedWatermark)
        self.FPLabel.adjustSize()
    def initUI(self):
        W,H = 1000,600
        STARTXY = (200,200)
        LX,LY,RX,RY = (STARTXY[0],STARTXY[1],STARTXY[0]+W,STARTXY[1]+H)

        self.WMButton = QPushButton("Watermark!",self)
        self.WMButton.move(0,H/2) 
        self.WMButton.clicked.connect(lambda: self.callWatermarker(self.selectedFP,self.selectedWatermark))


        
        self.SelectFolderButton = QPushButton("Select Folder(s)",self)
        self.SelectFolderButton.clicked.connect(lambda: self.selectFolder())
        self.SelectFolderButton.move(300,H/2)

        self.SelectFileButton = QPushButton("Select File(s)",self)
        self.SelectFileButton.clicked.connect(lambda: self.selectFile())
        self.SelectFileButton.move(200,H/2)

        self.SelectWatermarkButton = QPushButton("Select Watermark",self)
        self.SelectWatermarkButton.clicked.connect(lambda: self.selectWatermark())
        self.SelectWatermarkButton.move(100,H/2)

        self.selectedFP = []
        self.selectedWatermark = "wm.png"

        self.FPLabel = QLabel("; ".join(self.selectedFP),self)
        self.FPLabel.move(200,H/2+50)
#        self.FPLabel.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Minimum)
        self.FPLabel.adjustSize()
  #      self.FPLabel.resize(200,200)
        self.WMLabel = QLabel(self.selectedWatermark,self)
        self.WMLabel.move(100,H/2+50)

        self.setGeometry(LX,LY,RX,RY)
        self.setWindowTitle('Watermark Images')
    
        self.show()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = WMGui()
    sys.exit(app.exec_())
