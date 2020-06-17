#Main file launching the GUI and calling the deeplearning algorithms

import os
import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets                     # uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, 
                             QLabel, QVBoxLayout)              # +++
import datetime

 

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(725, 586)
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

        self.thick = QtWidgets.QPushButton(Form)
        self.thick.setObjectName("thick")
        self.verticalLayout.addWidget(self.thick)

        self.thin = QtWidgets.QPushButton(Form)
        self.thin.setObjectName("thin")
        self.verticalLayout.addWidget(self.thin)

        self.statlabel = QtWidgets.QLabel(Form,alignment=QtCore.Qt.AlignCenter)
        self.statlabel.setObjectName("statlabel")
        self.statlabel.resize(10, 40)
        self.verticalLayout.addWidget(self.statlabel)
        self.verticalLayout.setAlignment(self.statlabel,  QtCore.Qt.AlignTop)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form",     "Cam view"))
        self.control_bt.setText(_translate("Form", "Start streaming"))
        self.capture.setText(_translate("Form",    "Capture"))
        self.thick.setText(_translate("Form",    "Thick smear detection"))
        self.thin.setText(_translate("Form",    "Thin smear detection"))
        self.statlabel.setText(_translate("Form",    "Nothing is happening"))


class video (QtWidgets.QDialog, Ui_Form):
    def __init__(self):
        super().__init__()                  

#        uic.loadUi('test2.ui',self)                           # ---
        self.setupUi(self)                                     # +++
        self.showFullScreen()
        self.control_bt.clicked.connect(self.start_webcam)
        self.capture.clicked.connect(self.capture_image)
       # self.capture.clicked.connect(self.startUIWindow)       # - ()

  #      self.image_label.setScaledContents(True)

        self.cap = None                                        #  -capture <-> +cap
        self.streaming()

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
            self.statlabel.setText("Streaming")
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
        path = r'./'                         # 
        if flag:
           # QtWidgets.QApplication.beep()
            datetime_object = datetime.datetime.now() 
            print(datetime_object.strftime("%d_%m_%Y_%H:%M:%S"))
            name =  datetime_object.strftime("%d_%m_%Y_%H:%M:%S") + ".jpg"
            cv2.imwrite(os.path.join(path, name), frame)
            self.statlabel.setText("Image Captured")
            self._image_counter += 1
            self.cap.release()
            self.cap = None   
            self.flag = 0

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

    def startUIWindow(self):
        self.Window = UIWindow()                               # - self
        self.setWindowTitle("DeepMalaria")

#        self.setCentralWidget(self.Window)
#        self.show()
### +++ vvv
        self.Window.ToolsBTN.clicked.connect(self.goWindow1)

        self.hide()
        self.Window.show()

    def goWindow1(self):
        self.show()
        self.Window.hide()
 

if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = video()
    window.setWindowTitle('main code')
    window.show()
    sys.exit(app.exec_())
