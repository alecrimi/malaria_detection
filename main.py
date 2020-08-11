#Main file launching the GUI and calling the deeplearning algorithms

import os
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets                     # uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget,    QLabel, QVBoxLayout,QLineEdit,QMessageBox)              # +++
 
from PyQt5.QtGui import QPixmap

import datetime

from pymongo import MongoClient

#Name current file in analysis
name =''

##################################### Layout classes
#Layout Insertingdata
class SetData(QWidget):
    def __init__(self, parent=None):
        super(SetData, self).__init__(parent)

        path = r'data/' 
        self.labelImage = QLabel(self)
        self.pixmap = QPixmap(os.path.join(path, 'res_' + name))
        self.smaller_pixmap =self.pixmap.scaled(450, 450, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.labelImage.setPixmap( self.smaller_pixmap)
        self.labelImage.move(10, 10)
 
        self.textlabel = QLabel(self)
        self.textlabel.setText("Insert ID patient")
        self.textlabel.move(500, 40)

        self.textbox = QLineEdit(self)
        self.textbox.move(500, 60)
        self.textbox.resize(120,30)


        self.Save = QPushButton("Save", self)
        self.Save.move(100, 350)


        self.back = QPushButton("Back", self)
        self.back.move(250, 450)

        self.Save.setEnabled(False);
        self.textbox.textChanged.connect(self.disableButton)

    def disableButton(self):
       if len(self.textbox.text()) > 0:
          self.Save.setEnabled(True);



#Layout 3 analysis
class Analysis(QWidget):
    def __init__(self, parent=None):
        super(Analysis, self).__init__(parent)

        #self.labelImage = QLabel(self)
        #self.pixmap = QPixmap("microscope.png")
        #self.smaller_pixmap =self.pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        #self.labelImage.setPixmap( self.smaller_pixmap)
        #self.labelImage.move(50, 100)

        self.thick = QPushButton("Thick smear", self)
        self.thick.move(100, 350)

        self.labelImage = QLabel(self)
        self.pixmap = QPixmap("thinandthick.jpg")
        #self.smaller_pixmap =self.pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.labelImage.setPixmap( self.pixmap)
        self.labelImage.move(50, 100)

        self.thin = QPushButton("Thin smear", self)
        self.thin.move(400, 350)

        self.back = QPushButton("Back", self)
        self.back.move(250, 450)

#Layout 2 starting menu
class UIToolTab(QWidget):
    def __init__(self, parent=None):
        super(UIToolTab, self).__init__(parent)

        self.labelImage = QLabel(self)
        self.pixmap = QPixmap("microscope.png")
        self.smaller_pixmap =self.pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.labelImage.setPixmap( self.smaller_pixmap)
        self.labelImage.move(50, 100)

        self.CPSBTN = QPushButton("Acquire Data", self)
        self.CPSBTN.move(100, 350)


        self.labelImage = QLabel(self)
        self.pixmap = QPixmap("folders.png")
        self.smaller_pixmap =self.pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
        self.labelImage.setPixmap( self.smaller_pixmap)
        self.labelImage.move(350, 100)

        self.database = QPushButton("Look up database", self)
        self.database.move(400, 350)


 

#layout1 where images are captured
class Ui_Form(QWidget):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        #Form.resize(725, 586)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.image_label = QtWidgets.QLabel(Form,alignment=QtCore.Qt.AlignCenter)
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")
        self.verticalLayout.addWidget(self.image_label)
 
        self.control_bt = QtWidgets.QPushButton(Form)
        self.control_bt.setObjectName("control_bt")
        self.verticalLayout.addWidget(self.control_bt)

        self.capture = QtWidgets.QPushButton(Form)
        self.capture.setObjectName("capture")
        self.verticalLayout.addWidget(self.capture)

#        self.thick = QtWidgets.QPushButton(Form)
#        self.thick.setObjectName("thick")
#        self.verticalLayout.addWidget(self.thick)

#        self.thin = QtWidgets.QPushButton(Form)
#        self.thin.setObjectName("thin")
#        self.verticalLayout.addWidget(self.thin)


   #     self.statlabel = QtWidgets.QLabel(Form,alignment=QtCore.Qt.AlignCenter)
   #     self.statlabel.setObjectName("statlabel")
   #     self.statlabel.resize(10, 40)
   #     self.verticalLayout.addWidget(self.statlabel)
   #     self.verticalLayout.setAlignment(self.statlabel,  QtCore.Qt.AlignTop)

        self.back = QtWidgets.QPushButton(Form)
        self.back.setObjectName("back")
        self.verticalLayout.addWidget(self.back)
 
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form",     "Capturing"))
        self.control_bt.setText(_translate("Form", "Start streaming"))
        self.capture.setText(_translate("Form",    "Capture"))
     #   self.thick.setText(_translate("Form",    "Thick smear detection"))
     #   self.thin.setText(_translate("Form",    "Thin smear detection"))
     #   self.statlabel.setText(_translate("Form",    "Nothing is happening"))
        self.back.setText(_translate("Form",    "Back"))
######################################################################################

####################### Windows classes ##############################################
 
class StartWindow(QMainWindow):
    def __init__(self, parent=None):
        super(StartWindow, self).__init__(parent)
        self.setGeometry(50, 50, 640, 480)
        #self.showFullScreen()
        #self.setFixedSize(400, 450)
        self.startUIToolTab()

    def startUIToolTab(self):
        self.ToolTab = UIToolTab(self)
        self.setWindowTitle("StartWindow")
        self.setCentralWidget(self.ToolTab)
        self.ToolTab.CPSBTN.clicked.connect(self.startUIWindow)
        self.show()
 
    def startUIWindow(self):
        self.Window = Video(self)
        self.setWindowTitle("UIWindow")
        #self.setCentralWidget(self.Window)f
        #self.Window.capture.clicked.connect(self.startUIToolTab)
        self.show()

        self.hide()
        self.Window.show()

class AnalysisWindow(QMainWindow):
    def __init__(self, parent=None):
        super(AnalysisWindow, self).__init__(parent)
        self.setGeometry(50, 50, 640, 480)
        #self.showFullScreen()
        #self.setFixedSize(400, 450)
        self.startUIToolTab()

    def startUIToolTab(self):
        self.ToolTab = Analysis(self)
        self.setWindowTitle("Analysis")
        self.setCentralWidget(self.ToolTab)
        self.ToolTab.back.clicked.connect(self.startUIWindow)
        self.ToolTab.thick.clicked.connect(self.PerformThickAnalysis)
        self.ToolTab.thin.clicked.connect(self.PerformThinAnalysis)

        self.show()
 
    def startUIWindow(self):
        self.Window = Video(self) #???????
        self.setWindowTitle("Analysis")
        #self.setCentralWidget(self.Window)
        #self.Window.capture.clicked.connect(self.startUIToolTab)
        self.show()
        self.hide()
        self.Window.show()


    def PerformThickAnalysis(self):

        #Load data
        path = r'data/' 
        #original = cv2.imwrite(os.path.join(path, name), frame)
        img = cv2.imread(os.path.join(path, name),1)
        print('done')
        #perform Deeplearning classification

        cv2.imwrite(os.path.join(path, 'res_' + name), img)
        
        self.Window = SetDatasWindow(self)
        self.setWindowTitle("SetData")
        #self.setCentralWidget(self.Window)
        #self.Window.capture.clicked.connect(self.startUIToolTab)
        self.show()

        self.hide()
        self.Window.show()

    def PerformThinAnalysis(self):

        self.Window = SetDatasWindow(self)
        self.setWindowTitle("SetData")
        #self.setCentralWidget(self.Window)f
        #self.Window.capture.clicked.connect(self.startUIToolTab)
        self.show()

        self.hide()
        self.Window.show()


class SetDatasWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SetDatasWindow, self).__init__(parent)
        self.setGeometry(50, 50, 640, 480)
        #self.showFullScreen()
        #self.setFixedSize(400, 450)
        self.startUIToolTab()

    def startUIToolTab(self):
        self.ToolTab = SetData(self)
        self.setWindowTitle("SetData")
        self.setCentralWidget(self.ToolTab)
        self.ToolTab.back.clicked.connect(self.startUIWindow)
        self.ToolTab.Save.clicked.connect(self.saveData)
        self.show()
 
    def startUIWindow(self):
        self.Window = AnalysisWindow(self)
        self.setWindowTitle("Analysis")
        #self.setCentralWidget(self.Window)f
        #self.Window.capture.clicked.connect(self.startUIToolTab)
        self.show()
        self.hide()
        self.Window.show()

    def saveData(self):
        client = MongoClient()
        db = client.DATABASE_malaria
        collection = db.data
        new_id = self.ToolTab.textbox.text()
        post_id = collection.insert_one({"patient_id":new_id,"image_name":name}).inserted_id
        QMessageBox.about(self, "Database ok", "Data have been saved, you can proceed with another task")

class Video (QtWidgets.QDialog, Ui_Form):
    def __init__(self, parent=None):	
        super().__init__()                  
        self.setGeometry(50, 50, 640, 480)
#        uic.loadUi('test2.ui',self)                           # ---
        self.setupUi(self)                                     # +++
        #self.showFullScreen()
        self.control_bt.clicked.connect(self.start_webcam)
        self.capture.clicked.connect(self.capture_image)
        self.back.clicked.connect(self.startUIWindow)
  
       # self.capture.clicked.connect(self.startUIWindow)       # - ()

  #      self.image_label.setScaledContents(True)
        self.cap = None                                        #  -capture <-> +cap
        self.streaming()


    def startUIToolTab(self):
        self.ToolTab = UIToolTab(self)
        self.setWindowTitle("Video")
        #self.setCentralWidget(self.ToolTab)
        self.ToolTab.CPSBTN.clicked.connect(self.startUIWindow)
        self.show()
 

    def streaming(self):
        self.timer = QtCore.QTimer(self, interval=5)
        self.timer.timeout.connect(self.update_frame)
        self._image_counter = 0

    @QtCore.pyqtSlot()
    def start_webcam(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0) #default is 0
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    #        self.statlabel.setText("Streaming")
        self.timer.start()
        self.flag = 1
        self.streaming()

    @QtCore.pyqtSlot()
    def update_frame(self):
        if (self.flag):
           ret, image = self.cap.read()
           simage     = cv2.flip(image, 1)
           self.displayImage(image, True)

    @QtCore.pyqtSlot()
    def capture_image(self):
        flag, frame = self.cap.read()
        path = r'data/'                         # 
        if flag:
            # QtWidgets.QApplication.beep()
            global name
            datetime_object = datetime.datetime.now() 
            print(datetime_object.strftime("%d_%m_%Y_%H:%M:%S"))
            name =  datetime_object.strftime("%d_%m_%Y_%H:%M:%S") + ".jpg"
            cv2.imwrite(os.path.join(path, name), frame)
           # self.statlabel.setText("Image Captured")
            self._image_counter += 1
            self.cap.release()
            self.cap = None   
            self.flag = 0
#            self.startUIWindow()
            self.startAnalysis()

    def displayImage(self, img, window=True):
        qformat = QtGui.QImage.Format_Indexed8
        if len(img.shape)==3 :
            if img.shape[2]==4:
                qformat = QtGui.QImage.Format_RGBA8888
            else:
                qformat = QtGui.QImage.Format_RGB888
        outImage = QtGui.QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        if window:
            self.image_label.setPixmap(QtGui.QPixmap.fromImage(outImage))

 #   def startUIWindow(self):
 #       self.Window = UIWindow()                               # - self
 #       self.setWindowTitle("DeepMalaria")

#        self.setCentralWidget(self.Window)
#        self.show()
### +++ vvv
 #      self.Window.ToolsBTN.clicked.connect(self.goWindow1)
 
    def startUIWindow(self):
        self.Window = StartWindow(self)
        self.setWindowTitle("UIWindow")
        #self.setCentralWidget(self.Window)f
        #self.Window.capture.clicked.connect(self.startUIToolTab)
        self.show()

        self.hide()
        self.Window.show()



    def startAnalysis(self):
        self.Window = AnalysisWindow(self)
        self.setWindowTitle("Analysis")
        #self.setCentralWidget(self.Window)f
        #self.Window.capture.clicked.connect(self.startUIToolTab)
        self.show()

        self.hide()
        self.Window.show()

    def goWindow1(self):
        self.show()
        self.Window.hide()
 

if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = StartWindow()
    window.setWindowTitle('main code')
    window.show()
    sys.exit(app.exec_())
